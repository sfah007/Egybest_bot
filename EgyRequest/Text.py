commands = '''
start - ابدأ بالبحث عن فيلمك او مسلسلك المفضل
help - لطلب المساعدة ومعرفة المزيد عن هذا البوت
cancel - لإلغاء امر قائم حاليًا
'''

command_prevent_message = '''
لا يمكنك إستعمال أوامر أخرى في هذه المرحلة، إذا كنت تريد إستعمال أمر أخر إضغط على **/cancel**، أو بإمكانك الإستمرار في هذا الأمر.
'''

all_prevent_message = '''
لا يمكنك إستعمال أوامر أخرى أو الكتابة في هذه المرحلة، إذا كنت تريد إستعمال أمر أخر أو الكتابة إضغط على **/cancel**، أو بإمكانك الإستمرار في هذا الأمر.
'''

cancel_nothing = '''
لا يوجد أمر نشط للإلغاءه. لم أكن أفعل أي شيء على أي حال...

يمكنك ايضًا الضغط على **/help** للحصول على المساعدة ورؤية قائمة الأوامر.
'''

def cancel_message(command):

    return f'''
تم إلغاء أمر {command}. اى شئ اخر استطيع القيام به من اجلك؟

يمكنك ايضًا الضغط على **/help** للحصول على المساعدة ورؤية قائمة الأوامر.
'''

def select_type_message(show):
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
'''




