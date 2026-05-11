"""initial normalized schema
Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-11
"""
from alembic import op
import sqlalchemy as sa
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    user_role = sa.Enum("EMPLOYEE", "STUDENT", "ORG_ADMIN", "ADMIN", name="userrole")
    rec_type = sa.Enum("COURSE", "CERTIFICATION", "PROJECT", "PRACTICE", name="recommendationtype")
    skill_cat = sa.Enum("MANDATORY", "OPTIONAL", "ADVANCED", name="skillcategory")
    user_role.create(op.get_bind(), checkfirst=True); rec_type.create(op.get_bind(), checkfirst=True); skill_cat.create(op.get_bind(), checkfirst=True)
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("email", sa.String(255), nullable=False), sa.Column("full_name", sa.String(255), nullable=False), sa.Column("hashed_password", sa.String(255), nullable=False), sa.Column("role", user_role, nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table("skills", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(120), nullable=False), sa.Column("taxonomy", sa.String(120), nullable=False), sa.Column("demand_score", sa.Float(), nullable=False), sa.Column("salary_impact", sa.Float(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_skills_name", "skills", ["name"], unique=True)
    op.create_table("resumes", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("filename", sa.String(255), nullable=False), sa.Column("storage_path", sa.String(500), nullable=False), sa.Column("parsed_text", sa.Text(), nullable=False), sa.Column("extracted_profile", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_resumes_user_id", "resumes", ["user_id"])
    op.create_table("job_descriptions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("title", sa.String(255), nullable=False), sa.Column("company", sa.String(255)), sa.Column("raw_text", sa.Text(), nullable=False), sa.Column("required_skills", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_job_descriptions_owner_id", "job_descriptions", ["owner_id"]); op.create_index("ix_job_descriptions_title", "job_descriptions", ["title"])
    op.create_table("assessments", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("job_description_id", sa.Integer(), sa.ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False), sa.Column("match_percentage", sa.Float(), nullable=False), sa.Column("confidence_score", sa.Float(), nullable=False), sa.Column("missing_skills", sa.JSON(), nullable=False), sa.Column("priority_skills", sa.JSON(), nullable=False), sa.Column("proficiency_estimates", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_assessments_user_id", "assessments", ["user_id"]); op.create_index("ix_assessments_job_description_id", "assessments", ["job_description_id"])
    op.create_table("learning_paths", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("assessment_id", sa.Integer(), sa.ForeignKey("assessments.id", ondelete="SET NULL")), sa.Column("title", sa.String(255), nullable=False), sa.Column("timeline_weeks", sa.Integer(), nullable=False), sa.Column("milestones", sa.JSON(), nullable=False), sa.Column("progress", sa.Float(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_learning_paths_user_id", "learning_paths", ["user_id"])
    op.create_table("recommendations", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("learning_path_id", sa.Integer(), sa.ForeignKey("learning_paths.id", ondelete="CASCADE"), nullable=False), sa.Column("skill_name", sa.String(120), nullable=False), sa.Column("type", rec_type, nullable=False), sa.Column("title", sa.String(255), nullable=False), sa.Column("provider", sa.String(120)), sa.Column("url", sa.String(500)), sa.Column("rank_score", sa.Float(), nullable=False), sa.Column("duration_hours", sa.Integer(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_recommendations_learning_path_id", "recommendations", ["learning_path_id"]); op.create_index("ix_recommendations_skill_name", "recommendations", ["skill_name"])
    op.create_table("analytics_events", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("actor_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL")), sa.Column("event_name", sa.String(120), nullable=False), sa.Column("payload", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_analytics_events_actor_id", "analytics_events", ["actor_id"]); op.create_index("ix_analytics_events_event_name", "analytics_events", ["event_name"])
    op.create_table("job_skills", sa.Column("job_description_id", sa.Integer(), sa.ForeignKey("job_descriptions.id", ondelete="CASCADE"), primary_key=True), sa.Column("skill_id", sa.Integer(), sa.ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True), sa.Column("category", skill_cat, nullable=False), sa.Column("weight", sa.Float(), nullable=False), sa.UniqueConstraint("job_description_id", "skill_id", name="uq_job_skill"))

def downgrade() -> None:
    for table in ["job_skills", "analytics_events", "recommendations", "learning_paths", "assessments", "job_descriptions", "resumes", "skills", "users"]: op.drop_table(table)
    sa.Enum(name="skillcategory").drop(op.get_bind(), checkfirst=True); sa.Enum(name="recommendationtype").drop(op.get_bind(), checkfirst=True); sa.Enum(name="userrole").drop(op.get_bind(), checkfirst=True)
