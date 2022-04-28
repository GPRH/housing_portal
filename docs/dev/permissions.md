# Permissions

Permissions in the Housing Portal are organized on a **city** level within the Django [permissions system](https://docs.djangoproject.com/en/2.2/topics/auth/default/#permissions-and-authorization). When the application is first deployed, the `.env` file is read by the backend. A django setting `PORTAL_CITIES` is populated by the corresponding `.env` variable `PORTAL_CITIES`. For each city in `PORTAL_CITIES` a cusom `view_{city}` permission is created in the authentication backend. This is created at deployment time by a migration at `backend/apps/users/migrations/0002_add_permissions.py`.

Using another migration at `backend/apps/users/migrations/0003_add_groups.py` a set of django `Groups` are created. For each portal instance a `{country}GovernmentUserGroup` is created, so for example if the Housing Portal instance is for Paraguay, a `ParaguayGovernmentUserGroup` will be created. A `ParaguayAdminUserGroup` group will also be created.

For each city in `PORTAL_CITIES` a `UserGroup{city}` will be created and the `view_{city}` permission will be assigned to each corresponding city group.

Finally each of the `UserGroup{city}` groups are added to the Government and Admin groups respecively, meaning that any user assigned to either the `Government` or `Admin` user group will be able to view all cities in the portal deployment. Users assigned to the `Admin` group will also have the authorization to add new users to the system and to assign user permssions and groups.

### Users

A special `Admin` user is created at deployment time by a migration at `backend/apps/users/migrations/0004_create_super_user.py`. This users login email is `admin@admin.com` and the default password is `admin`. **_This password should be changed when the portal is first deployed_**. The password can also be set using the `ADMIN_USER_PASS` setting in the `.env` file. This user is a django `superuser` and is automatically added to the `GovernmentUserGroup` and the `AdminUserGroup`. As indicated above, since this user is assigned to the `Admin` group, they can also add new users to the system using the django [Admin](admin.md) interface.
