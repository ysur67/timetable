"""empty message

Revision ID: 437fe0abb5dd
Revises: 6f68c97aa742
Create Date: 2024-04-18 01:42:49.406369

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "437fe0abb5dd"
down_revision: str | None = "6f68c97aa742"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("lesson_hash_constraint_unique", "lesson", ["hash_"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("lesson_hash_constraint_unique", "lesson", type_="unique")
    # ### end Alembic commands ###