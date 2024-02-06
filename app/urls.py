from django.urls import path,include
from . import views
urlpatterns = [
    path("",views.indexPage,name="indexPage"),
    path("signup/",views.signupPage,name="signupPage"),
    path("registeruser/",views.registerUser,name="registeruser"),
    path("otppage/",views.otpPage,name="otppage"),
    path("otpverify/",views.otpVerification,name="otpverify"),
    path("loginpage/",views.loginPage,name="loginPage"),
    path("login/",views.login,name="login"),
    path("profiledata/<int:pk>",views.profileDetails,name="profiledata"),
    path("updateprofile/<int:pk>",views.updateProfile,name="updateprofile"),
    path("canJobListPage/",views.canJobListPage,name="canJobListPage"),
    path("canJobApplyPage/<int:pk>",views.canJobApplyPage,name="canJobApplyPage"),
    path("canJobApply/",views.canJobApply,name="canJobApply"),

    # company urls
    path("compIndex/",views.compIndexPage,name="compIndex"),
    path("postJobPage/",views.postJobPage,name="postJobPage"),
    path("postJob/<int:pk>",views.postJob,name="postJob"),
    path("jobPostListPage/<int:pk>",views.jobPostListPage,name="jobPostListPage"),
    path("compLogout/",views.compLogout,name="compLogout"),
    path("appliedJobPage/",views.appliedJobPage,name="appliedJobPage"),

    # logout
    path("logout/",views.logout,name="logout"),

    # admin
    path("adminIndexPage/",views.adminIndexPage,name="adminIndexPage"),
    path("jobadmin/",views.adminLoginPage,name="adminLoginPage"),
    path("adminLogin/",views.adminLogin,name="adminLogin"),
    path("adminCanList/",views.adminCanList,name="adminCanList"),
    path("adminCompList/",views.adminCompList,name="adminCompList"),

    # resend otp
    path("resendOtp/<email>",views.resendOtp,name="resendOtp"),
]
