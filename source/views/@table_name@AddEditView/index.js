import React from 'react';
import { userRoleClient } from 'src/components/RoleHelper'
import { default as @|table_name|@AddEditBaseView } from './base'
import { useNavigate } from 'react-router-dom';
import { useLocation } from "react-router";
import {
  Box,
  Grid,
  makeStyles,
} from '@material-ui/core';
import Page from 'src/components/Page';
import ProtectedButton from 'src/helpers/Button.js';
import { withTranslation } from 'react-i18next';
import { observer } from "mobx-react"
import store from "./store"
import MtmTab from "./mtmTabs"

const @|table_name|@AddEditView = observer(
  class @|table_name|@AddEditView extends React.Component {

    render() {
      const { t } = this.props
      const translate = t

      return (
        <Page title={translate('label:@|table_name|@AddEditView.entityTitle')}>
          <@|table_name|@AddEditBaseView {...this.props}>

            @|template_mtm_has_mtm|@

            <Grid container xs={12} md={@|template_mtm_has_mtm_grid|@} style={{ margin: 0, justifyContent: "flex-end" }}>
              <Box display="flex" p={2}>
                <Box m={2}>
                  <ProtectedButton
                    variant="contained"
                    id="id_@|table_name|@SaveButton"
                    color="save"
                    name={'@|table_name|@AddEditView.save'}
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
                    id="id_@|table_name|@CancelButton"
                    color="cancel"
                    name={'@|table_name|@AddEditView.cancel'}
                    onClick={() => {
                      this.props.navigate(process.env.REACT_APP_SUB_ROUTE + '/user/@|table_name|@', { replace: true })
                    }}
                  >
                    {translate("common:cancel")}
                  </ProtectedButton>
                </Box>
              </Box>
            </Grid>
          </@|table_name|@AddEditBaseView>
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
  return <@|table_name|@AddEditView {...props} navigate={navigate} classes={classes} id={idParam} />
}

export default withTranslation()(WithAllProps)
