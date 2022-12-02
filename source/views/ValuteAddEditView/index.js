import React from 'react';
import { userRoleClient } from 'src/components/RoleHelper'
import { default as ValuteAddEditBaseView } from './base'
import { useNavigate } from 'react-router-dom';
import { useLocation } from "react-router";
import {
  Box,
  Grid,
  makeStyles,
} from '@material-ui/core';
import Page from 'src/components/Page';
import ProtectedButton from 'src/helpers/Button.js';

//! Проверить необходимость 
//
import { withTranslation } from 'react-i18next';
import { observer } from "mobx-react"
import store from "./store"
import MtmTab from "./mtmTabs"

const ValuteAddEditView = observer(
  class ValuteAddEditView extends React.Component {


   render() {
    var roleName = 'ValuteAddEditView';
    var roles = userRoleClient();
    const { t } = this.props
    const translate = t


     return (
        <Page title={translate('label:ValuteAddEditView.entityTitle')}>
          <ValuteAddEditBaseView {...this.props}>

            {/* start MTM */}
            {store.id > 0 && <MtmTab />}
            {/* end MTM */}


            <Grid container xs={12} md={store.id == 0 ? 6 : 12} style={{ margin: 0, justifyContent: "flex-end" }}>
              <Box display="flex" p={2}>

            <Box m={2}>
              <ProtectedButton
               variant="contained"
		id="id_ValuteSaveButton"
                roles={roles}
                color="save"
                name={roleName + '.save'}
                roleName={roleName + '.save'}
                onClick={() => {
                      store.onSaveClick(this.props)
                }}
              >
                {translate("common:save")}
              </ProtectedButton>
            </Box>

            <Box m={2}>
              <ProtectedButton
                variant="contained"
		id="id_ValuteCancelButton"
                roles={roles}
                    color="cancel"
                name={roleName + '.cancel'}
                roleName={roleName + '.cancel'}
                onClick={() => {
                      this.props.navigate(process.env.REACT_APP_SUB_ROUTE + '/user/Valute', { replace: true })
                }}
              >
                {translate("common:cancel")}
              </ProtectedButton>
            </Box>

          </Box>
            </Grid>
          </ValuteAddEditBaseView>
      </Page>
    );
  }
  }
)

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    height: '100%',
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3)
  }
}));

function WithAllProps(props) {
  let navigate = useNavigate();
  let query = useQuery();
  let classes = useStyles();
  let id = query.get("id")
  let idParam = id != null || id != 0 ? id : 0
  store.id = idParam
  return <ValuteAddEditView {...props} navigate={navigate} classes={classes} id={idParam} />
}

export default withTranslation()(WithAllProps)
