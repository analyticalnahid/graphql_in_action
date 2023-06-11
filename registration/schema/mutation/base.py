import graphene
from .registration import UserRegistrationMutation, VerifyOTPMutation
from .login import UserLoginMutation, UserForgetPasswordMutation, UserResetPasswordMutation
from .profile import ChangePasswordMutation, AccountUpdateMutation, AccountDeletionMutation


class Mutation(graphene.ObjectType):
    register_user = UserRegistrationMutation.Field(description="Register a new user")
    verify_otp = VerifyOTPMutation.Field(description="Verify OTP")
    login_user = UserLoginMutation.Field(description="Login a user")
    forget_pass = UserForgetPasswordMutation.Field(description="Forget password")
    reset_pass = UserResetPasswordMutation.Field(description="Reset password")
    change_password = ChangePasswordMutation.Field(description="Change password")
    account_update = AccountUpdateMutation.Field(description="Update account")
    delete_user = AccountDeletionMutation.Field(description="Delete account")

    def resolve_reset_pass(self, info, input_data):
        return UserResetPasswordMutation.mutate(root=None, info=info, input_data=input_data)
