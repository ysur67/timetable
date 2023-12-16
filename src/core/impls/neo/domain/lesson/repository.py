import hashlib
from typing import final

from neo4j import AsyncSession

from core.domain.lesson.repository import LessonRepository
from core.models.lesson import Lesson
from scraping.clients import lessons_client
from scraping.schemas.lesson import LessonSchema


@final
class NeoLessonRepository(LessonRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, lesson: Lesson) -> Lesson | None:
        subject = lesson.subject.title if lesson.subject else "None"
        teacher = lesson.teacher.name if lesson.teacher else "None"
        classroom = lesson.classroom.name if lesson.classroom else "None"
        date_ = lesson.date_.isoformat()
        hash_ = hashlib.sha512(
            lesson.group.title + subject + teacher + classroom + date_,
        )
        stmt = """
            match (l:Lesson)-[:TAUGHT_TO]-(g:Group)
            optional match
                (l:Lesson)-[:TOPIC_OF]-(s:Subject),
                (l:Lesson)-[:TAUGHT_BY]-(t:Teacher),
                (l:Lesson)-[:HELD_IN]-(c:Classroom)
            return l, s, t, c;
        """
        result = await self._session.run(stmt)
        return result

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
                link: $lesson.link
            })-[:TAUGHT_TO]-(g);
        """
        lesson_dict = lesson.model_dump(mode="json")
        _ = await self._session.run(
            create_stmt,
            parameters={
                "group": lesson_dict,
                "lesson": lesson.model_dump(mode="json"),
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
