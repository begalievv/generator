import React from 'react';
import { userRoleClient } from 'src/components/RoleHelper';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router';
import { withTranslation } from 'react-i18next';
import {
  makeStyles
} from '@material-ui/core';
import ProtectedButton from 'src/helpers/Button.js';
import ValuteAddEditBaseView from './base';
import DialogActions from '@material-ui/core/DialogActions';
import TabPanel from './mtmTabs';
import DialogForm from 'src/helpers/Dialog';
import i18n from 'i18next';
import AlertDialog from 'src/helpers/AlertDialogs';
import Loader from 'src/components/loader';
import store from "./store"
import { observer } from "mobx-react"

const ValuteAddEditView = observer(
class ValuteAddEditView extends React.Component {

  render() {
    const { t } = this.props;
    const translate = t;

    var roleName = 'ValuteAddEditView';
    var roles = userRoleClient();

    const actions = <DialogActions>
      <ProtectedButton
        color="save"
        variant="contained"
        roles={roles}
	id="id_ValuteSaveButton"
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
        id="id_ValuteCancelButton"
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
        entityTitle={translate("label:ValuteAddEditView.entityTitle")}
          controllerName={"Valute"}
        actions={actions}>

        <ValuteAddEditBaseView
            isPopup={true}
          id={this.props.id}
        >
        </ValuteAddEditBaseView>

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
  let query = useQuery();
  let classes = useStyles();
  if (props.id != null || props.id != 0) {
    store.id = props.id
  }
  return <ValuteAddEditView {...props} navigate={navigate} classes={classes} />;
}

export default withTranslation(['label'])(WithAllProps);
