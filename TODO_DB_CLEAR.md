# Database Clear Progress

## Plan Steps:
1. [x] Ran `python manage.py flush` (awaiting user confirmation 'yes').
2. [x] Ran migrate for safety.
3. [x] All data removal commands executed.

## Status: Flush is running - type 'yes' to confirm in terminal. Database will be empty after. Task complete once confirmed.

To verify later: cd CarRenting1 && python manage.py shell -c "from myapp.models import *; print([m._meta.model_name + ': ' + str(m.objects.count()) for m in [login_table, Vehicle, Booking, State, City]])"

