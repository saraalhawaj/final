# from django_comments.models import Comment
# from django.contrib.contenttypes.models import ContentType
# from posts.models import Post
# from django.contrib.sites.models import Site
# from django.contrib.auth.models import User
# from django.utils import timezone
# Comment.objects.create(
#      content_type=ContentType.objects.get_for_model(Post),
#      object_pk=Post.objects.first(),
#      site=Site.objects.get(id=1),
#      user = User.objects.get(id=1),
#      user_name = User.objects.get(id=1).username,
#      comment = "Hey work",
#      submit_date = timezone.now()
# )