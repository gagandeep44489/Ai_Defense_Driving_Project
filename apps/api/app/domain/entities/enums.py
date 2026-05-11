from enum import StrEnum
class UserRole(StrEnum):
    EMPLOYEE = "employee"
    STUDENT = "student"
    ORG_ADMIN = "org_admin"
    ADMIN = "admin"
class SkillCategory(StrEnum):
    MANDATORY = "mandatory"
    OPTIONAL = "optional"
    ADVANCED = "advanced"
class RecommendationType(StrEnum):
    COURSE = "course"
    CERTIFICATION = "certification"
    PROJECT = "project"
    PRACTICE = "practice"
