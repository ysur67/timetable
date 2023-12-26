from neo4j import AsyncSession

from core.models.lesson import Lesson


async def create_lesson(session: AsyncSession, lesson: Lesson) -> Lesson:
    # TODO: use hash maybe
    stmt = """
        match (group:Group)
            where group.id = $group.id
        create (lesson:Lesson {
            id: $lesson.id,
            date: $lesson.date_,
            time_start: $lesson.time_start,
            time_end: $lesson.time_end,
            link: $lesson.link,
            note: $lesson.note
        })-[:TAUGHT_TO]->(group);
    """
    await session.run(
        stmt,
        parameters={
            "lesson": lesson.model_dump(mode="json"),
            "group": lesson.group.model_dump(mode="json"),
        },
    )
    return lesson
