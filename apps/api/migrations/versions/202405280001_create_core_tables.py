"""create core domain tables"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "202405280001"
down_revision = None
branch_labels = None
depends_on = None


user_role_enum = sa.Enum("admin", "analyst", "viewer", name="user_role")
detector_mode_enum = sa.Enum("binary", "multiclass", name="detector_mode")
image_query_answer_enum = sa.Enum("YES", "NO", "UNKNOWN", name="image_query_answer")
alert_status_enum = sa.Enum("open", "ack", "resolved", name="alert_status")
alert_channel_enum = sa.Enum("email", "sms", "webhook", name="alert_channel")
escalation_status_enum = sa.Enum("open", "ack", "resolved", name="escalation_status")


UUID = postgresql.UUID(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID, primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=True),
        sa.Column("role", user_role_enum, nullable=False),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)

    op.create_table(
        "detectors",
        sa.Column("id", UUID, primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("mode", detector_mode_enum, nullable=False),
        sa.Column("query", sa.Text(), nullable=False),
        sa.Column("confidence_threshold", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_by_id", UUID, nullable=False),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "streams",
        sa.Column("id", UUID, primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("rtsp_url", sa.Text(), nullable=False),
        sa.Column("zone_masks", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "image_queries",
        sa.Column("id", UUID, primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("detector_id", UUID, nullable=False),
        sa.Column("rtsp_source_id", UUID, nullable=True),
        sa.Column("snapshot_url", sa.Text(), nullable=False),
        sa.Column("answer", image_query_answer_enum, nullable=True),
        sa.Column("answer_score", sa.Float(), nullable=True),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["detector_id"], ["detectors.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["rtsp_source_id"], ["streams.id"], ondelete="SET NULL"),
    )

    op.create_table(
        "alerts",
        sa.Column("id", UUID, primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("detector_id", UUID, nullable=False),
        sa.Column("image_query_id", UUID, nullable=False),
        sa.Column("status", alert_status_enum, nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("channel", alert_channel_enum, nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["detector_id"], ["detectors.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["image_query_id"], ["image_queries.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "escalations",
        sa.Column("id", UUID, primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("alert_id", UUID, nullable=False),
        sa.Column("assigned_to_id", UUID, nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("status", escalation_status_enum, nullable=False),
        sa.ForeignKeyConstraint(["alert_id"], ["alerts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["assigned_to_id"], ["users.id"], ondelete="SET NULL"),
    )

    op.create_table(
        "annotations",
        sa.Column("id", UUID, primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("image_query_id", UUID, nullable=False),
        sa.Column("annotator_id", UUID, nullable=True),
        sa.Column("label_json", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["image_query_id"], ["image_queries.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["annotator_id"], ["users.id"], ondelete="SET NULL"),
    )


def downgrade() -> None:
    op.drop_table("annotations")
    op.drop_table("escalations")
    op.drop_table("alerts")
    op.drop_table("image_queries")
    op.drop_table("streams")
    op.drop_table("detectors")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    alert_channel_enum.drop(op.get_bind(), checkfirst=False)
    alert_status_enum.drop(op.get_bind(), checkfirst=False)
    image_query_answer_enum.drop(op.get_bind(), checkfirst=False)
    escalation_status_enum.drop(op.get_bind(), checkfirst=False)
    detector_mode_enum.drop(op.get_bind(), checkfirst=False)
    user_role_enum.drop(op.get_bind(), checkfirst=False)
