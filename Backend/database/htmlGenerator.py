'''Module that generates html code\n
Main functions:
- getWorkplacesHTML, getChannelsHTML, getMessagesHtml'''
# other libs
from html import escape as saveHTML
# my libs
from database.extractor import getUserWorkplacesColumn, getWorkplaceChannelsColumn, getWorkplaceFieldById, getWorkplaceChannelsFieldByChannelId


def getWorkplacesHTML(nameDB: str, user_id: str) -> str:
    '''Returns html code with workplaces buttons'''

    ids = getUserWorkplacesColumn(nameDB, user_id, 'global_id')
    workplace_names = getUserWorkplacesColumn(nameDB, user_id, 'workplace_name')

    # user haven`t workplaces
    if len(workplace_names) == 0:
        return '<button onclick="show_workplaces_adder()">Add Workplace</button>'

    if [""] in [ids, workplace_names]:
        return '<button>Something wrong with our servers. 🫤</button>'

    result = ""
    for index, id in enumerate(ids):
        result += f"<button onclick='getChannels({id})'>{saveHTML(workplace_names[index])}</button>"
    return result


def getChannelsHTML(nameDB: str, workplace_id: str) -> str:
    '''Returns html code with channels buttons'''

    ids = getWorkplaceChannelsColumn(nameDB, workplace_id, 'id')
    channel_names = getWorkplaceChannelsColumn(nameDB, workplace_id, 'channel_name')
    workplace_name = getWorkplaceFieldById(nameDB, workplace_id, 'workplace_name')

    result = f'''
        <h3>
            {workplace_name}
            <button onclick="show_channels_adder()" class="add_channel" >+</button>
        </h3>
        <div class="channels_area">
    '''

    # workplace haven`t channels
    if len(channel_names) == 0:
        return result + '<button onclick="show_channels_adder()">Add Channel</button></div>'

    # bad database request
    if [""] in [ids, channel_names, [workplace_name]]:
        return '<button>Something wrong with our servers. 🫤</button>'
    
    for index, id in enumerate(ids):
        result += f"<button onclick='getChat({id}, true)'>{saveHTML(channel_names[index])}</button>"
    return result + "</div>"


def getMessagesHtml(nameDB: str, workplace_id: str, channel_id: str) -> str:
    '''Returns Html code with chat'''

    channel_name = getWorkplaceChannelsFieldByChannelId(nameDB, workplace_id, channel_id, 'channel_name')
    result = f'''
        <h3>{channel_name}</h3>
        <div class="chat_area">
            <messages class="messages">
    '''
    result += getWorkplaceChannelsFieldByChannelId(nameDB, workplace_id, channel_id, 'chat')
    result += '''
            </messages>
        </div>
        '''
    return result