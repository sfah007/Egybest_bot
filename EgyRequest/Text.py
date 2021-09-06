commands = '''
start - ابدأ بالبحث عن فيلمك او مسلسلك المفضل
help - لطلب المساعدة ومعرفة المزيد عن هذا البوت
cancel - لإلغاء امر قائم حاليًا
'''

command_prevent_message = '''
لا يمكنك إستعمال أوامر أخرى في هذه المرحلة، إذا كنت تريد إستعمال أمر أخر إضغط على **/cancel**، أو بإمكانك الإستمرار في هذا الأمر.
'''
cancel_nothing_message = '''
لا يوجد أمر نشط للإلغاءه. لم أكن أفعل أي شيء على أي حال...

يمكنك ايضًا الضغط على **/help** للحصول على المساعدة ورؤية قائمة الأوامر.
'''

cancel_message = '''
لقد تم الخروج من هذه العملية بنجاح، يمكنك الآن البدء في أمر جديد عبر الضغط على /start.

يمكنك ايضًا الضغط على **/help** للحصول على المساعدة ورؤية قائمة الأوامر.
'''

quality_wait_message = '''
الآن يتم استخراج الروابط، الرجاء الإنتظار لمدة لا تزيد عن 10 ثواني.

ملاحظة: **لن يتم تنفيذ أي امر خلال عملية استخراج الروابط**.
'''

sleep_message = '''
اممممممم ...
ليس هناك ما علي فعله، إليك بعض الإقتراحات التي يمكنني توفيرها لك:

- ابدأ اللآن بالضغط على **/start** لمشاهدة أو تحميل فيلمك أو مسلسلك المفضل.

- يمكنك ايضًا الضغط على **/help** لمعرفة المزيد عن هذا البوت.
'''

timeout_message = '''
لقد إنتهت المدة المحددة لهذه العملية بدون أي تفاعل (**وهي 3 ساعات**).

اذا كنت تريد البدأ والبحث من جديد يمكنك الضغط على **/start**.
'''

help_message = '''
هذا اقصى ما يمكنني المساعدة به:

ما يمكن للبوت فعله:
- مشاهدة وتحميل جميع الأفلام والمسلسلات الأجنبية والعربية المتوفرة على موقع Egybest مجانًا وبدون اعلانات.

الأوامر المتوفرة:
/start : ابدأ بالبحث عن فيلمك او مسلسلك المفضل.
/help : لطلب المساعدة ومعرفة المزيد عن هذا البوت.
/cancel : لإلغاء امر قائم حاليًا.

شروط الإستخدام:
-الإشتراك في قناة @Egybot_Community

تم البرمجة بواسطة:
@H_hisham

شكر خاص للمشرفين:
@m5kyd
@R5d3b

'''

def select_type_message(show, add=None):
    l = []

    for i in range(0, len(show['info']),2):
        l.append(f'● {show["info"][i]} : {show["info"][i + 1]}')
    l = '\n\n'.join(l)

    return f'''
[{show['show']['name']} - {show['show']['type']}]({show['show']['img']})

{l}

القصة :

{show['story']}

تقييم المشاهدين : {show['rate']}

**{' - '.join(add) if add else ''}**
'''



