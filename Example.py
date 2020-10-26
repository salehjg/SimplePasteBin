import SimplePasteBin as helper

pb = helper.SimplePasteBin(
    username='<YOUR USERNAME>',
    password='<YOUR PASSWORD>',
    api_key='<YOUR API KEY>',
    is_verbose=True)

ret_val = pb.login()
ret_val += pb.create_paste('title1', 'my paste content', 'N', 'public')

if ret_val == 0:
    exit(0)
else:
    exit(1)
