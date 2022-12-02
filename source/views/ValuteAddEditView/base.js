import React from 'react';
import { userApiClient, baseUrl } from 'src/components/ApiHelper';
import { userRoleClient } from 'src/components/RoleHelper';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router';
import { validate } from './valid';
import {
  Card,
  CardContent,
  CardHeader,
  Divider,
  Paper,
  Grid,
  Box,
  Button,
  makeStyles,
FormControlLabel,
  Container,
} from '@material-ui/core';
import BaseLookup from 'src/components/BaseLookup';
import ProtectedTextField from 'src/helpers/TextField.js';
import { withTranslation } from 'react-i18next';
import SubtitlesOutlinedIcon from '@material-ui/icons/SubtitlesOutlined';
import DescriptionOutlinedIcon from '@material-ui/icons/DescriptionOutlined';
import CodeOutlinedIcon from '@material-ui/icons/CodeOutlined';
import DynamicFeedOutlinedIcon from '@material-ui/icons/DynamicFeedOutlined';
import store from "./store"
import { observer } from "mobx-react"


const localStorageKeyHideDictionaryCode = 'hideDictionaryCode'

export const BaseView = observer(
class BaseView extends React.Component {

  componentDidMount() {
      store.doLoad(this.props.id)
  }
  
  render() {
    var roleName = 'ValuteAddEditView';
    var roles = userRoleClient();
    const { t } = this.props;
    const translate = t;
	let md = this.props.isPopup ? 12 : 6

    return (
        <Container maxWidth='xl'>
          <Grid container md={md} xs={12} spacing={0}>

          <form id="id_ValuteForm" name="name_ValuteForm" autoComplete='off' noValidate>
           <Paper elevation={7} style={{ width: '100%' }}>
            <Card>
              <CardHeader className={this.props.classes.header} title={<span id="id_f_Valute_title_name">{translate('label:ValuteAddEditView.entityTitle')}</span>} />
              <Divider />
              <CardContent>
                   <Grid container xs={12} spacing={3} style={{ margin: 0 }}>
		    <Grid item md={12} xs={12}>
	              <ProtectedTextField
                        fullWidth
                        label={translate('label:ValuteAddEditView.name')}
                        name="name"
			id="id_f_Valute_name"
                          onChange={(event)=>store.handleChange(event)}
                          value={store.name}
                          variant="outlined"
                          roles={roles}
                          icon={<SubtitlesOutlinedIcon />}
                           roleName={roleName + '.name'}
                             
                        helperText={store.errorname}
                        error={store.errorname != ''}
                      />
                    </Grid>
		    <Grid item md={12} xs={12}>
	              <ProtectedTextField
                        fullWidth
                        label={translate('label:ValuteAddEditView.description')}
                        name="description"
			id="id_f_Valute_description"
                          onChange={(event)=>store.handleChange(event)}
                          value={store.description}
                          variant="outlined"
                          roles={roles}
                          icon={<SubtitlesOutlinedIcon />}
                           roleName={roleName + '.description'}
                             
                        helperText={store.errordescription}
                        error={store.errordescription != ''}
                      />
                    </Grid>
		    <Grid item md={12} xs={12}>
	              <ProtectedTextField
                        fullWidth
                        label={translate('label:ValuteAddEditView.code')}
                        name="code"
			id="id_f_Valute_code"
                          onChange={(event)=>store.handleChange(event)}
                          value={store.code}
                          variant="outlined"
                          roles={roles}
                          icon={<SubtitlesOutlinedIcon />}
                           roleName={roleName + '.code'}
                             
                        helperText={store.errorcode}
                        error={store.errorcode != ''}
                      />
                    </Grid>
		    <Grid item md={12} xs={12}>
	              <ProtectedTextField
                        fullWidth
                        label={translate('label:ValuteAddEditView.queueNumber')}
                        name="queueNumber"
			id="id_f_Valute_queueNumber"
                          onChange={(event)=>store.handleChange(event)}
                          value={store.queueNumber}
                          variant="outlined"
                          roles={roles}
                          icon={<SubtitlesOutlinedIcon />}
                           roleName={roleName + '.queueNumber'}
                             
                        helperText={store.errorqueueNumber}
                        error={store.errorqueueNumber != ''}
                      />
                    </Grid>

                  </Grid>
               </CardContent>
            </Card>
            </Paper>
          </form>
        </Grid>
            {this.props.children}
      </Container>
    );
  }
  }
)

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

const useStyles = makeStyles((theme) => ({
  header: {
    backgroundColor: theme.palette.headerForm.dark,
  }
}));

function ValuteAddEditBaseView(props) {
  let navigate = useNavigate();
  let query = useQuery();
  let classes = useStyles();
  return <BaseView {...props} navigate={navigate} classes={classes} />;
}

export default withTranslation()(ValuteAddEditBaseView);
