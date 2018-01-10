from django.db import models
from .models import UserProfile, Comment


class Flagged(models.Model):
    flagged_by = models.ForeignKey(UserProfile)
    # offensive, violent/threat, against the rules, bullying
    reason_description = models.CharField()
    flag_count = models.IntegerField()
    flagged_to_comment = models.ForeignKey(FlaggedComment)
    flagged_to_user = models.ForeignKey(FlaggedUser)
    flagged_to_question = models.ForeignKey(FlaggedQuestion)

    @classmethod
    def add_flag(cls):
        # FORMULA : Total Comments
        cls.flag_count += 1

    @classmethod
    def remove_flag(cls):
        cls.flag_count -= 1


class FlaggedComment(models.Model):
    comment_id = models.OneToOneField(Comment)
    flagged = models.OneToOneField(Flagged)


class FlaggedUser(models.Model):
    is_banned_user = models.BooleanField()
    flagged_question = models.ManyToManyField(FlaggedQuestion)
    flagged_question_count = models.IntegerField()

    @classmethod
    def get_flag_count(cls):
        pass


class FlaggedQuestion(models.Model):
    is_age_restricted = models.BooleanField()


class BlockedUser(models.Model, FlaggedUser):
    """
    Ubiq. Language:
        Blocker = User that is blocking
        Blocked = User blocked
    Description:
        The Blocker won't see the Blocked details, and
        vice versa. This includes not seeing their
        comments, or on News Feed.
        Blocked users are viewed by Blocker on a list
        They can choose to unblock.

    """
    user_doing_the_blocking = models.ForeignKey(User)
    blocked_user_id = models.CharField()
    taking_a_break_from_this_user = models.BooleanField()

    @classmethod
    def unblock_user(cls):
        """
            check the JSON of the Blocker's block list, and see if that id exists in the
            JSON currently. If it is, then remove it.
        """
        if cls.blocked_user_id is cls.user_doing_the_blocking.blockedlist.blocked_user_id:
            # TODO: Then you will remove that id from the JSON.
            for user in cls.user_doing_the_blocking.blocked_users_list:
                if user == cls.blocked_user_id:
                    pass
