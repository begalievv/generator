import React from 'react';
import {
  Box,
  Container,
  makeStyles
} from '@material-ui/core';
import Page from 'src/components/Page';
import PageGrid from 'src/components/PageGrid';
import PopupGrid from 'src/components/PopupGrid';
import @|table_name|@AddEditView from 'src/views/@|table_name|@/@|table_name|@AddEditView/popupForm';
import { withTranslation } from 'react-i18next';
import { observer } from "mobx-react"
import store from "./store"


const @|table_name|@ListView = observer(
  class @|table_name|@ListView extends React.Component {

    componentDidMount() {
      @|template_index_load_function|@
    }
    
    render() {
      const { t } = this.props
      const translate = t

      const columns = [
        @|template_index_columns|@
      ];

      const type = '@|template_index_is_mtm_popup|@';
      let component = null;
      switch (type) {
        case 'form':
          component = <PageGrid
            title={translate("label:@|table_name|@ListView.@|table_name|@")}
            subtitle={translate("label:@|table_name|@ListView.@|table_name|@")}
            onItemDeleted={() => @|template_index_load_function|@}
            columns={columns}
            data={store.data}
            layout='user'
            controllerName="@|table_name|@" />
          break;
        case 'popup':
          component = <React.Fragment>
            <PopupGrid
              title={translate("label:@|table_name|@ListView.@|table_name|@")}
              subtitle={translate("label:@|table_name|@ListView.@|table_name|@")}
              onButtonAddEditClick={(id) => store.onButtonAddEditClick(id)}
              onItemDeleted={() => @|template_index_load_function|@}
              columns={columns}
              data={store.data}
              layout='user'
              controllerName="@|table_name|@" />

            <@|table_name|@AddEditView
              isPopup={true}
              openPanel={store.openPanel}
              id={store.currentId}
              onBtnOkClick={() => {
                @|template_index_load_function|@
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
        <Page title={translate("label:@|table_name|@ListView.@|table_name|@")}>

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
  return <@|table_name|@ListView {...props} classes={classes} />
}

export default withTranslation(['label'])(WithAllProps)
