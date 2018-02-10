from rest_framework import serializers
from main.models import *


from rest_framework_jwt.settings import api_settings

class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = CustomUser
		fields = '__all__'

	def create(self, validated_data):
		email = validated_data['email']
		password = validated_data['password']
		major = validated_data['major']
		course = validated_data['course']
		new_user = User(email=email)
		new_user = User(major=major)
		new_user = User(course=course)
		new_user.set_password(password)
		
		new_user.save()
		return validated_data

class UserLoginSerializer(serializers.Serializer):
	email = serializers.CharField()
	password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	token = serializers.CharField(allow_blank=True, read_only=True)

	def validate(self, data):
		user_obj = None

		email = data.get('email')
		password = data.get('password')

		if email == '':
			raise serializers.ValidationError("A email is required to login.")
		
		user = User.objects.filter(email=email)
		if user.exists():
			user_obj = user.first()
		else:
			raise serializers.ValidationError("This email is not valid.")
		
		if user_obj:
			if not user_obj.check_password(password):
				raise serializers.ValidationError("This credentials, please try again.")

		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

		payload = jwt_payload_handler(user_obj)
		token = jwt_encode_handler(payload)
		
		data["token"] = token
		return data

class UserDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model = CustomUser
		fields = '__all__'

# class MyfeedListSerializer(serializers.ModelSerializer):
# 	detail = serializers.HyperlinkedIdentityField(
# 		view_name = "api:detail",
		
# 		)
# 	class Meta:
# 		model = Myfeed
# 		fields = '__all__'


# class MyfeedCreateSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Myfeed
# 		fields = '__all__'



# class MyfeedDetailSerializer(serializers.ModelSerializer):
# 	author = UserDetailSerializer()
# 	comments = serializers.SerializerMethodField()
	
# 	class Meta:
# 		model = Myfeed
# 		fields = '__all__'

# 	def get_replys(self, obj):
# 		reply_queryset = Reply.objects.filter(object_pk=obj.id)
# 		replys = ReplyListSerializer(reply_queryset, many=True).data
# 		return replys



class MyfeedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Myfeed
        fields = ['feed','book','timestamp', 'major', 'course']


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['timestamp', 'reply','myfeed','user']
class MyfeedDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Myfeed
        fields = ['user',  'feed', 'slug']

class MyfeedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Myfeed
        fields = [ 'feed','book','timestamp','major', 'course']

class ReplyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['timestamp', 'reply','myfeed','user','major', 'course']
