from neo4j import AsyncSession

from core.domain.lesson.repository import LessonRepository
from core.impls.neo.mappers.neo_record_to_domain_mapper import NeoRecordToDomainMapper
from core.models import Lesson


class NeoLessonRepository(LessonRepository):
    def __init__(self, session: AsyncSession, mapper: NeoRecordToDomainMapper) -> None:
        self._session = session
        self._mapper = mapper

    async def get(self, lesson: Lesson) -> Lesson | None:
        stmt = """
            match (lesson:Lesson)-[:TAUGHT_TO]-(group:Group)-[:BELONGS_TO]-(educational_level:EducationalLevel)
                where lesson.hash = $hash
            optional match (lesson:Lesson)-[:TOPIC_OF]-(subject:Subject)
            optional match (lesson:Lesson)-[:TAUGHT_BY]-(teacher:Teacher)
            optional match (lesson:Lesson)-[:HELD_IN]-(classroom:Classroom)
            return
                lesson,
                group,
                subject,
                teacher,
                classroom,
                educational_level;
        """
        result = await self._session.run(
            stmt,
            parameters={"hash": lesson.get_hash()},
        )
        record = await result.single()
        if record is None:
            return None
        return self._mapper.map_lesson(record.data())

    # TODO: Воспользоваться merge?
    async def create(self, lesson: Lesson) -> Lesson:
        create_stmt = """
            match (g:Group)
                where g.id = $group.id
            create (l:Lesson {
                id: $lesson.id,
                date: $lesson.date_,
                time_start: $lesson.time_start,
                time_end: $lesson.time_end,
                link: $lesson.link,
                note: $lesson.note,
                hash: $hash
            })-[:TAUGHT_TO]->(g);
        """
        lesson_dict = lesson.model_dump(mode="json")
        _ = await self._session.run(
            create_stmt,
            parameters={
                "group": lesson.group.model_dump(mode="json"),
                "lesson": lesson_dict,
                "hash": lesson.get_hash(),
            },
        )
        if (classroom := lesson.classroom) is not None:
            stmt = """
                match (l:Lesson), (c:Classroom)
                    where l.id = $lesson.id and c.id = $classroom.id
                create (l)-[:HELD_IN]->(c);
            """
            await self._session.run(
                stmt,
                parameters={
                    "lesson": lesson_dict,
                    "classroom": classroom.model_dump(mode="json"),
                },
            )
        if (teacher := lesson.teacher) is not None:
            stmt = """
                match (l:Lesson), (t:Teacher)
                    where l.id = $lesson.id and t.id = $teacher.id
                create (l)-[:TAUGHT_BY]->(t);
            """
            await self._session.run(
                stmt,
                parameters={
                    "lesson": lesson_dict,
                    "teacher": teacher.model_dump(mode="json"),
                },
            )
        if (subject := lesson.subject) is not None:
            stmt = """
                match (l:Lesson), (s:Subject)
                    where l.id = $lesson.id and s.id = $subject.id
                create (l)-[:TOPIC_OF]->(s);
            """
            await self._session.run(
                stmt,
                parameters={
                    "lesson": lesson_dict,
                    "subject": subject.model_dump(mode="json"),
                },
            )
        return lesson
