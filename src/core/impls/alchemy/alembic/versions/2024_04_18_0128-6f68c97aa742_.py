"""empty message

Revision ID: 6f68c97aa742
Revises: 872298049119
Create Date: 2024-04-18 01:28:54.815564

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6f68c97aa742"
down_revision: str | None = "872298049119"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("classroom_title_constraint_unique", "classroom", ["title"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("classroom_title_constraint_unique", "classroom", type_="unique")
    # ### end Alembic commands ###
