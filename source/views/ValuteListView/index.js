import React from 'react';
import { userRoleClient } from 'src/components/RoleHelper'
import {
  Box,
  Container,
  makeStyles
} from '@material-ui/core';
import Page from 'src/components/Page';
import PageGrid from 'src/components/PageGrid';
import PopupGrid from 'src/components/PopupGrid';
import ValuteAddEditView from 'src/views/Valute/ValuteAddEditView/popupForm';
import { withTranslation } from 'react-i18next';
import { observer } from "mobx-react"
import store from "./store"


const ValuteListView = observer(
class ValuteListView extends React.Component {

  componentDidMount() {
      store.loadValutes();
  }

  render() {
    var roleName = 'ValuteListView';
    var roles = userRoleClient();
    const { t } = this.props
    const translate = t


    const columns = [
      {
        name:"name",
        id:"id_g_Valute_name",
        label: translate("label:ValuteListView.name"),
        options: {
          filter: true,
          customHeadLabelRender: (columnMeta) => (<div name={"name_g_Valute_name_title"}>{columnMeta.label}</div>),
          customBodyRenderLite: (dataIndex) => {
              if (dataIndex >= store.data.length) return null;
              return <div name={"name_g_Valute_name"}>{store.data[dataIndex].name}</div>
          }
        }
      },
      {
        name:"description",
        id:"id_g_Valute_description",
        label: translate("label:ValuteListView.description"),
        options: {
          filter: true,
          customHeadLabelRender: (columnMeta) => (<div name={"name_g_Valute_description_title"}>{columnMeta.label}</div>),
          customBodyRenderLite: (dataIndex) => {
              if (dataIndex >= store.data.length) return null;
              return <div name={"name_g_Valute_description"}>{store.data[dataIndex].description}</div>
          }
        }
      },
      {
        name:"code",
        id:"id_g_Valute_code",
        label: translate("label:ValuteListView.code"),
        options: {
          filter: true,
          customHeadLabelRender: (columnMeta) => (<div name={"name_g_Valute_code_title"}>{columnMeta.label}</div>),
          customBodyRenderLite: (dataIndex) => {
              if (dataIndex >= store.data.length) return null;
              return <div name={"name_g_Valute_code"}>{store.data[dataIndex].code}</div>
          }
        }
      },
      {
        name:"queueNumber",
        id:"id_g_Valute_queueNumber",
        label: translate("label:ValuteListView.queueNumber"),
        options: {
          filter: true,
          customHeadLabelRender: (columnMeta) => (<div name={"name_g_Valute_queueNumber_title"}>{columnMeta.label}</div>),
          customBodyRenderLite: (dataIndex) => {
              if (dataIndex >= store.data.length) return null;
              return <div name={"name_g_Valute_queueNumber"}>{store.data[dataIndex].queueNumber}</div>
          }
        }
      },
    ];

    const type = 'form';
    let component = null;
    switch (type) {
      case 'form':
        component = <PageGrid
          title={translate("label:ValuteListView.Valute")}
          subtitle={translate("label:ValuteListView.entityTitle")}
          onItemDeleted={() => store.loadValutes()}
          columns={columns}
            data={store.data}
          layout='user'
          roles={roles}
          roleName={roleName + '.list'}
          controllerName="Valute" />
        break;
      case 'popup':
        component = <React.Fragment>
          <PopupGrid
            title={translate("label:ValuteListView.Valute")}
            subtitle={translate("label:ValuteListView.entityTitle")}
              onButtonAddEditClick={(id) => store.onButtonAddEditClick(id)}
              onItemDeleted={() => store.loadValutes()}
            columns={columns}
            data={store.data}
            layout='user'
            roles={roles}
            rolename={roleName + '.list'}
            controllerName="Valute" />

          <ValuteAddEditView
	    isPopup={true}	
              openPanel={store.openPanel}
              id={store.currentId}
              onBtnOkClick={() => {
                store.loadValutes()
                store.closePanel()
              }}
              onBtnCancelClick={() => {
                store.closePanel()
              }}
          />
        </React.Fragment>
        break;
    }
    return (
      <Page title={translate("label:ValuteListView.Valute")}>

        <Container maxWidth={false}>

          {component}

        </Container>
      </Page>
    );
  }
  }
)


const useStyles = makeStyles((theme) => ({
}));

function WithAllProps(props) {
  let classes = useStyles();
  return <ValuteListView {...props} classes={classes} />
}

export default withTranslation(['label'])(WithAllProps)
