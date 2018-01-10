"""Copyright (C) 2017 Camino Tech
 # *
 # * This file is part of Decissions Project.
 # *
 # * Decissions Project can not be copied and/or distributed without the express
 # * permission of Camino Tech
"""
import uuid

from django.db import models
# from django.contrib.gis.db.models.fields import PointField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


# USING ABRACT USER MAKES THIS APP NOT REUSABLE < THIS IS MAIN APP >


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    unique_id = models.CharField(max_length=120, blank=True, unique=True, default=uuid.uuid4)
    birthday = models.DateTimeField()
    first_name = models.CharField()
    last_name = models.CharField()
    profile_picture = models.CharField()
    hometown = models.CharField()
    current_city = models.CharField()
    # may be too aggressive
    income_status = models.CharField()
    # income_amount = models.DecimalField()
    # will have to look at followers and match for better results (maybe recommend), this could be multiples
    # Users can choose to display
    # { user_education: { fields: [ title: "", place: "", intitution_name: "", date_finished: "", date_entered: "",
    #  gpa: "", student_email = "", ]}}
    educational_background = JSONField()
    password = models.CharField()
    email = models.EmailField()
    gender = models.CharField()
    marital_status = models.CharField()
    biography = models.TextField()
    industries_or_occupations = JSONField()
    phone_number = models.CharField()
    ethnicity = models.CharField()
    page_layout = models.CharField()  # uses colors.py
    banner = models.CharField()  # link to image
    # Maybe?
    social_status = models.CharField()
    # - the permissions, and verifications that this user  has
    verified = models.BooleanField() # SHARED FROM ROLES
    time_membership_expires = models.DateTimeField() # SHARED FROM ROLES
    milestones = JSONField()
    blocked_users_list = JSONField()
    is_private = models.BooleanField()
    personal_website_links = JSONField()
    following = models.ManyToManyField(FriendUser)
    followed = models.ManyToManyField(FriendUser)
    user_to_questions = models.ForeignKey(UserToQuestions)
    user_to_data = models.ForeignKey(UserToData)
    user_to_roles = models.ForeignKey(UserToRoles)


class FriendUser(models.ForeignKey):
    logged_in_users_id = models.ForeignKey(User)
    friend_id_from_user = models.ForeignKey(User)
    follows_user = models.BooleanField()
    followed_by_user = models.BooleanField()

    @classmethod
    def accept_follow_request(cls, user_id):
        if cls.friend_id_from_user.is_private:
            """return send_request()"""
            pass
        else:
            cls.follows_user = True
            # LOGGED IN USER IS ACCEPTING REQUEST AND GAINS A FOLLOWER
            cls.logged_in_users_id.followed.append(cls.friend_id_from_user)
            # USER WHO WANTS TO FOLLOW LOGGED IN USER IS NOW FOLLOWING LOGGED IN USER
            cls.friend_id_from_user.following.append(cls.logged_in_users_id)

    @classmethod
    def unfollow_a_user(cls):
        cls.follows_user = False
        cls.logged_in_users_id.followed.remove(cls.friend_id_from_user)
        cls.friend_id_from_user.following.remove(cls.logged_in_users_id)


class UserToQuestions(models.Model):
    questions_users_have_voted_on = models.ManyToManyField(Question)
    user_id = models.ForeignKey(User)
    #Checks if user already voted on that question
    voted_trigger = models.BooleanField()
    voteResult = models.CharField()
    date_voted = models.DateField()
    is_anonymous_vote = models.BooleanField()

    @classmethod
    def anonymous_vote(cls):
        if cls.is_anonymous_vote is True:
            # Do not display on News Feed / User Profile Page
            # if its anonymous then the question voted on still shows
            # but the decision of the user isn't
            cls.is_anonymous_vote = False
        else:
            # display on News Feed / User Profile Page
            # could possibly all go through as REST API
            # then it would just change the trigger for that question
            # individually
            cls.is_anonymous_vote = True


class UserToRoles(models.Model):
    user_type = models.CharField()


class Roles(models.Model):
    premium = models.BooleanField()
    transaction_history = models.JSONField()
    previous_roles = models.JSONField()


class Question(models.Model):
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    unique_id = models.CharField(max_length=120, blank=True, unique=True, default=uuid.uuid4)
    title = models.CharField()
    # section contains JSON with photo link, and choices
    sections = models.ManyToManyField(QuestionSection)
    # to check if it has already been voted)
    question_to_user = models.ForeignKey(QuestionToUser)
    number_of_views = models.BigIntegerField()
    number_of_votes = models.IntegerField()
    revoting_allowed = models.BooleanField()
    question_to_comments = models.ForeignKey(QuestionComments)
    question_to_category = models.ForeignKey(QuestionsToCategory)


class QuestionSection(models.Model):
    title = models.CharField()
    question_id = models.ForeignKey(Question)
    photo_link = models.CharField()
    number_of_votes = models.BigIntegerField()
    comments_section_id = models.ForeignKey(QuestionComments)


class QuestionToUser(models.Model):
    user = models.ForeignKey(User)


class Comment(models.Model):
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    comment_id = models.CharField(max_length=200, blank=True, unique=True, default=uuid.uuid4)

    flagged_to_comments = models.ForeignKey(flagged.FlaggedComment)
    comment_text = models.CharField()
    user_id = models.ForeignKey(User)
    question_to_comments = models.ForeignKey(QuestionComments)
    upvote_count = models.IntegerField()
    comment_is_visible = models.BooleanField(default=True)

    @classmethod
    def reply(cls):
        # FOR THE MOMENT THERE WILL BE NO REPLYING TO COMMENTS
        pass

    @classmethod
    def post_a_comment(cls):
        pass

    @classmethod
    def delete_your_own_comment(cls, user_id):
        if user_id is cls.user_id:
            cls.comment_is_visible = False

    @classmethod
    def upvote_comment(cls):
        cls.upvote_count += 1


class QuestionComments(models.Model):
    """
    What makes this Comment-type Unique?

    Multiple comment sections per question section,
    so each instance of this class will be one comment section per question section
    """
    question_section_id = models.ForeignKey(Question)
    all_of_the_comments_in_a_section = models.ManyToManyField(Comment)

    @classmethod
    def sort_by_most_upvotes(self):
        """ query all comments in this section, and rank the top three """
        pass
    @classmethod
    def sort_by_most_recent(self):
        pass
    @classmethod
    def get_top_three_comments(self):
        """ useful for when keywords come in, to also pull data and Search Engine based on comments"""
        pass


class UserProfileComments(models.Model):
    owner_user_id = models.ForeignKey(User)
    visitor_user_id = models.ForeignKey(User)
    profile_page_comment = models.ForeignKey(Comment)


class NewsFeedComments(models.Model):
    pass


class UserToData(models.Model):
    # could be GPS
    user = models.ManyToManyField(User)
    # user_location = PointField(lon=0, lat=0)
    data = models.OneToOneField(Data)


class Data(models.Model):
    data_uuid = models.CharField(max_length=120, blank=True, unique=True, default=uuid.uuid4)
    question = models.ForeignKey(Question)
    # for retrieving everything from user
    user = models.ForeignKey(User)
    # for graph changes
    date_voted = models.DateField()


class QuestionsToCategory:
    assigned_categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_id = models.OneToOneField(Question)


class Category(models.Model):
    title = models.CharField()
