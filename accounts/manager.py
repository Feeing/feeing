from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager) :
    def create_user(self, name, username, phone, bank_account, password=None,**extra_fields) :
        # if not username :
        #     raise ValueError(_('The ID must be set'))
        # username = self.model.normalize_username(username)
        # name = self.model(name = name, **extra_fields)
        # user = self.model(username = username, **extra_fields)
        # phone = self.model(phone = phone, **extra_fields)
        # user.set_password(password)
        # user.save(using = self._db)
        # return user
        user = self.model(
            name = name,
            username = username,
            phone = phone,
            bank_account = bank_account,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, name, username, password, phone, bank_account, **extra_fields) :
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_active', True)

        # if extra_fields.get('is_staff') is not True :
        #     raise ValueError(_('Superuser must have is_staff=True.'))
        # if extra_fields.get('is_superuser') is not True :
        #     raise ValueError(_('Superuser must have is_superuser=True.'))
        # return self.create_user(name, username, phone, password, account_number, **extra_fields)
        user = self.create_user(
            name = name,
            username = username,
            password=password,
            phone = phone,
            bank_account = bank_account,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user