import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router';
import { withTranslation } from 'react-i18next';
import {
  makeStyles
} from '@material-ui/core';
import ProtectedButton from 'src/helpers/Button.js';
import @|table_name|@AddEditBaseView from './base';
import DialogActions from '@material-ui/core/DialogActions';
import DialogForm from 'src/helpers/Dialog';
import store from "./store"
import { observer } from "mobx-react"

const @|table_name|@AddEditView = observer(
  class @|table_name|@AddEditView extends React.Component {

    render() {
      const { t } = this.props;
      const translate = t;

      const actions = <DialogActions>
        <ProtectedButton
          color="save"
          variant="contained"
          roles={roles}
          id="id_@|table_name|@SaveButton"
          name={roleName + '.save'}
          roleName={roleName + '.save'}
          onClick={() => {
            store.onSaveClick(this.props)
          }}
        >
          {translate("common:save")}
        </ProtectedButton>
        <ProtectedButton
          color="cancel"
          variant="contained"
          id="id_@|table_name|@CancelButton"
          name={roleName + '.cancel'}
          roles={roles}
          roleName={roleName + '.cancel'}
          onClick={() => this.props.onBtnCancelClick()}
        >
          {translate("common:cancel")}
        </ProtectedButton>
      </DialogActions>

      return (
        <DialogForm
          openPanel={this.props.openPanel}
          entityTitle={translate("label:@|table_name|@AddEditView.entityTitle")}
          controllerName={"@|table_name|@"}
          actions={actions}>
          <@|table_name|@AddEditBaseView
            isPopup={true}
            id={this.props.id}
          >
          </@|table_name|@AddEditBaseView>
        </DialogForm>
      );
    }
  }
)

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

const useStyles = makeStyles((theme) => ({
}));

function WithAllProps(props) {
  let navigate = useNavigate();
  let classes = useStyles();
  if (props.id != null || props.id != 0) {
    store.id = props.id
  }
  return <@|table_name|@AddEditView {...props} navigate={navigate} classes={classes} />;
}

export default withTranslation(['label'])(WithAllProps);
