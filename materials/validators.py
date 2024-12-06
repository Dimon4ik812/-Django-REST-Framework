import re
from rest_framework.exceptions import ValidationError


class LinkToVideoValidator:
    """Валидатор для модели Lesson, поля video_link"""

    message = "Доступны только ссылки с youtube.com!"

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        youtube_pattern = r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]+$"
        tmp_field = dict(value).get(self.field)
        if not re.match(youtube_pattern, tmp_field):
            raise ValidationError(self.message)