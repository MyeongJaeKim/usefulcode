
# -----------------------------------------------------------------------
# AWS Crendentials
#
# Be aware of the security threaten if these keys would be leaked to bad people
# -----------------------------------------------------------------------

aws_credentials = {'stg_account':{'ACCESS_KEY':'key here', 'SECRET_KEY':'secret here'},
                   'prd_account':{'ACCESS_KEY':'key here', 'SECRET_KEY':'secret here'}}

# MUST BE SAME AS THE ACCOUNT NAME AND THEIR ORDERS ABOVE!
account_list = ['stg_account', 'prd_account']
