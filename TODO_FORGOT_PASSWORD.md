# Forgot Password Feature Progress

## Plan Steps:
1. [x] Read key files.
2. [x] Edit models.py + ran makemigrations.
3. [ ] Edit views.py.
4. [ ] Edit templates.
5. [x] Migrations started.
6. [ ] Test.

## Completed:
- Models updated with reset_token/reset_expiry, migrated 0012.
- Views.py: forgotpassword sends email, changepwdpage validates, changepwd updates.
- Templates: forgotpasswordpage.html ready, changepwdpage.html updated for reset (hidden token/email, new_pwd/confirm_pwd).

**To test:**
1. `cd CarRenting1 && python manage.py runserver`
2. Signup/login to create user (DB empty).
3. Visit /myapp/forgotpasswordpage/, submit email.
4. Check gmail inbox for link.
5. Click link, enter new/confirm pwd, submit.
6. Login with new pwd.

Feature ready! Close old flush terminal if done.


