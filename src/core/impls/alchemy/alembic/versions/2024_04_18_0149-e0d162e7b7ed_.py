"""empty message

Revision ID: e0d162e7b7ed
Revises: 437fe0abb5dd
Create Date: 2024-04-18 01:49:28.575664

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e0d162e7b7ed"
down_revision: str | None = "437fe0abb5dd"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("subject_title_constraint_unique", "subject", ["title"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("subject_title_constraint_unique", "subject", type_="unique")
    # ### end Alembic commands ###
