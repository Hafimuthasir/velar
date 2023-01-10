from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('register',register,name='register'),
    # path('login',login,name='login'),
    path('userhome',userhome,name='userhome'),
    path('feedPost',feedPosts,name='feedPost'),
    path('getUserPosts/<int:id>',getUserPosts,name='getUserPosts'),
    path('getOwnStory/<int:id>',getOwnStory,name='getOwnStory'),

    path('getProfileDatas/<int:userid>',getProfileDatas,name='getProfileDatas'),
    path('getStory',getStory,name='getStory'),
    path('getCurStory/<int:id>',getCurStory,name='getCurStory'),

    path('subComment',subComment,name='subComment'),
    path('LikePost',LikePost,name='LikePost'),
    path('uploadPost',uploadPost,name='uploadPost'),
    path('uploadStory',uploadStory,name='uploadStory'),

    path('follow',follow,name='follow'),
    path('followCheck',followCheck,name='followCheck'),
    path('ProfileCounts/<id>',ProfileCounts,name='ProfileCounts'),

    path('dummyPurchase',dummyPurchase,name='dummyPurchase'),
    path('DownloadFile/<str:filename>',DownloadFile,name='DownloadFile'),
    path('GetTestData',GetTestData,name='GetTestData'),
    path('addDownloadsCount',addDownloadsCount.as_view(),name='addDownloadsCount'),

    path ('GetExplorePosts/<str:section>',GetExplorePosts.as_view(),name='GetExplorePosts'),
    path ('GetLangPosts/<str:lang>',GetLangPosts.as_view(),name='GetLangPosts'),
    path ('GetAllSearch/<str:search>',GetAllSearch.as_view(),name='GetAllSearch'),
    path ('GetTrendingDownloads',GetTrendingDownloads.as_view(),name='GetTrendingDownloads'),



    path ('getUserNotFollowers/<int:id>',GetUserNotFollowers.as_view(),name='GetUserNotFollowers'),

    path('',getRoutes,name='routes'),
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
