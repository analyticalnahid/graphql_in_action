import graphene
from .registration import UserRegistrationMutation, VerifyOTPMutation
from .login import UserLoginMutation, UserForgetPasswordMutation, UserResetPasswordMutation
from .profile import ChangePasswordMutation, AccountUpdateMutation, AccountDeletionMutation


class Mutation(graphene.ObjectType):
    register_user = UserRegistrationMutation.Field()
    verify_otp = VerifyOTPMutation.Field()
    login_user = UserLoginMutation.Field()
    forget_pass = UserForgetPasswordMutation.Field()
    reset_pass = UserResetPasswordMutation.Field()
    change_password = ChangePasswordMutation.Field()
    account_update = AccountUpdateMutation.Field()
    delete_user = AccountDeletionMutation.Field()

    def resolve_reset_pass(self, info, input_data):
        return UserResetPasswordMutation.mutate(root=None, info=info, input_data=input_data)
