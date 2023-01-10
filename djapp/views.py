from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import *
from django.core.files import File
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
# Create your views here.


@api_view(['GET','POST'])       
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]  
    
    return Response(routes)
   

@api_view(['POST'])
def register(request):
  
        email = request.data.get('email')
        print ('j',email)
        checkem=User.objects.filter(email=email)
        if checkem:
            return Response('Email already exist')
        else:
            serializer = UserSerializers(data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(200)

# @api_view(['POST'])
# def login(request):
#     print('am login',request.data)
#     email = request.data['email']
#     password = request.data['password']
#     check = User.objects.filter(email=email,password=password).first()
#     if check:
#         user = 'True'
#         print('true')
#     else:
#         user = 'False'
#         print('false')
#     print("hj",check.id)
#     payload = {
#             'id':check.id,
#             'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
#             'iat':datetime.datetime.utcnow()
#         }
#     token = jwt.encode(payload,'secret',algorithm='HS256')

#     response = Response()
        
#     response.set_cookie(key='jwt',value=token,httponly=True)
    
#     response.data = {
#             'jwt':token,
            
#         }
#     print('lllloool')
#     tk = request.COOKIES.get('jwt')
#     print('mm',tk)
#     print('lll',response)
#     dec = jwt.decode(token,'secret',algorithms='HS256')
#     print ('ds',dec)
#     return response



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.first_name
        token['is_admin'] = user.is_admin
        if user.profile:
            token['profile'] = user.profile.url
        else:
            token['profile'] = "null"

        # ...
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
        
    

@api_view(['GET'])
def userhome(request):
    print('in userhome')
    return Response(200)

@api_view(['POST'])
def uploadPost(request):
    print('in up post')
    print(request.data)
    serializer = PostSerializer(data=request.data,partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
  
    return Response(200)


@api_view(['POST'])
def uploadStory(request):
    print('in up story')
    print(request.data)
    serializer = StorySerializer(data=request.data,partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save() 
    return Response(200)

@api_view(['GET'])
def feedPosts(request):
    print('lol in feed')
    allPost = Posts.objects.all().order_by('-id')
    serializer = PostSerializer(allPost,many=True)
    print('hai')

    # test = serializer.data
    # mydict = {k: test(v).encode("utf-8") for k,v in mydict.iteritems()}
    
    # test2 = test.decode('utf-16')
    # print(test2)
    return Response(serializer.data)

@api_view(['GET'])
def getStory(request):
    today = datetime.datetime.now() - datetime.timedelta(days=1)
    Use = Story.objects.filter(created_at__gte=today,).distinct('userid')
    # check = Use.('userid').distinct()
   
    serializer = StorySerializer(Use,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCurStory(request,id):
    print('lol in stry',request.data)
    today = datetime.datetime.now() - datetime.timedelta(days=1)
    Use = Story.objects.filter(userid=id,created_at__gte=today)
    serializer=StorySerializer(Use,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def subComment(request):
    print('lol in com',request.data)
    serializer=CommentSerializer(data=request.data,partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response('hai')


@api_view(['POST'])
def LikePost(request):
    print('in like maahn',request.data['user'])
    user = request.data['user']
    post = request.data['post']
    
    exist = Likes.objects.filter(user=user,post=post)
    if exist:        
        exist.delete()
        likecount = Posts.objects.get(id=post)
        print('jii',likecount.likes)
        if int(likecount.likes) > 0:
            likecount.likes=likecount.likes-1
            likecount.save()
        return Response(likecount.likes)
        
    else :
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        likecount = Posts.objects.get(id=post)
        likecount.likes=int(likecount.likes)+1
        likecount.save()
       
        return Response(likecount.likes)
       
    
@api_view(['GET','POST'])
def getUserPosts(request,id):
    print('33333',request.data)
    if request.data['section'] == 'all':
        posts = Posts.objects.filter(userid=id).order_by("-id")
        serializers = PostSerializer(posts,many=True)
        return Response(serializers.data)
    if request.data['section'] == 'files':
        posts = Posts.objects.filter(userid=id,is_z=True).order_by("-id")
        serializers = PostSerializer(posts,many=True)
        return Response(serializers.data)
    if request.data['section'] == 'primes':
        posts = Posts.objects.filter(userid=id,is_premium=True).order_by("-id")
        serializers = PostSerializer(posts,many=True)
        return Response(serializers.data)
    if request.data['section'] == 'purchases':
        posts = PremiumPurchases.objects.filter(userid=id).order_by("-id")
        serializers = MyPurchases(posts,many=True)
        return Response(serializers.data)

@api_view(['GET'])
def getOwnStory(request,id):
    today = datetime.datetime.now() - datetime.timedelta(days=1)
    Use = Story.objects.filter(userid=id,created_at__gte=today,)
    serializers = StorySerializer(Use,many=True)
    return Response(serializers.data)
    
    
@api_view(['GET'])
def getProfileDatas(request,userid):
    user = User.objects.get(id=userid)
    serializers = UserSerializers(user,many=True)
    return Response(200)



@api_view(['POST'])
def follow(request):
    
    check = Follow.objects.filter(follower=request.data['follower'],following = request.data['following'])
    if check:
        check.delete()
        return Response('unfollowed')
    else:
        print('infals')
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('followed')
        else:
            print(serializer.errors)
            return Response(serializer.errors)
            

@api_view(['POST'])
def followCheck(request):
    check = Follow.objects.filter(follower=request.data['follower'],following = request.data['following'])
    if check:
        return Response('Following')
    else:
        return Response('Follow')

@api_view(['GET'])
def ProfileCounts(request,id):
    uss = User.objects.get(id=id)
    serializer = UserSerializers(uss)
    return Response(serializer.data)
    

@api_view(['POST'])
def dummyPurchase(request):
    data=request.data
    serializer = PrimeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if serializer.is_valid:
        serializer.save()
        return Response('success')
    return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

@api_view(['GET'])
def DownloadFile(self,filename):
    # with open('reactapp/src/uploads/zpostfile/FACE_MASK_fG5rUZ1.rar') as f:
    zip_file = open('reactapp/src/uploads/zpostfile/'+filename, 'rb')
    response = HttpResponse(zip_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'foo.zip'
    return response

class addDownloadsCount(APIView):
    def post (self,request):
        check = AllDownloads.objects.filter(postid=request.data['postid'],userid=request.data['userid'])
        if check:
            return Response('Already In DList')
        else:
            serializer = DownloadsCountSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                countadd = Posts.objects.get(id=request.data['postid'])
                countadd.downloadsCount = countadd.downloadsCount + 1
                countadd.save()
                return Response("success")
        return Response('Something Went Wrong')


class GetExplorePosts(APIView):
    def get(self,request,section):
        try:
            if section == 'all':
                posts = Posts.objects.all()
                serializer = PostSerializer(posts,many=True)
                return Response(serializer.data)
            if section == 'files':
                posts = Posts.objects.filter(is_z=True)
                serializer = PostSerializer(posts,many=True)
                return Response(serializer.data)
            if section == 'primes':
                posts = Posts.objects.filter(is_premium=True)
                serializer = PostSerializer(posts,many=True)
                return Response(serializer.data)
            if section == 'trend':
                posts = Posts.objects.filter(lang='Python').order_by('-likes')
                serializer = PostSerializer(posts,many=True)
                return Response(serializer.data)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetLangPosts(APIView):
    def get(self,request,lang):
        posts = Posts.objects.filter(lang=lang)
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
        

class GetUserNotFollowers(APIView):
    def get(self,request,id):
        notfollowers = Follow.objects.exclude(follower=id)
        serializer=FollowSerializerGet(notfollowers,many=True)
        return Response(serializer.data)


class GetAllSearch(APIView):
    def get(self,request,search):
        posts = Posts.objects.filter(caption__icontains=search)
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)


@api_view(['GET'])
def GetTestData(request):
    return Response('done')
        # return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTrendingDownloads(APIView):
    def get(self,request):
        data = Posts.objects.filter(is_z=True).order_by('-downloadsCount')
        serializer = PostSerializer(data,many=True)
        return Response(serializer.data)

        
