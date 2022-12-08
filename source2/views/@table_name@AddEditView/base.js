import React from 'react';
import { userApiClient, baseUrl } from 'src/components/ApiHelper';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router';
import {
  Card,
  CardContent,
  CardHeader,
  Divider,
  Paper,
  Grid,
  Button,
  makeStyles,
  FormControlLabel,
  Container,
} from '@material-ui/core';
import BaseLookup from 'src/components/BaseLookup';
import ProtectedTextField from 'src/helpers/TextField.js';
import { withTranslation } from 'react-i18next';
import store from "./store"
import { observer } from "mobx-react"


export const BaseView = observer(
  class BaseView extends React.Component {

    componentDidMount() {
      store.doLoad(this.props.id)
    }

    render() {
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
                      @|template_base_fields|@
                      <Grid item md={12} xs={12}>
                        <ProtectedTextField
                          label={translate('label:ValuteAddEditView.name')}
                          name="name"
                          id="id_f_Valute_name"
                          onChange={(event) => store.handleChange(event)}
                          value={store.name}
                          variant="outlined"
                          helperText={store.errorname}
                          error={store.errorname != ''}
                        />
                      </Grid>

                      <Grid item md={12} xs={12}>
                        <BaseLookup
                          helperText={store.erroridCoordinateSystem}
                          error={store.erroridCoordinateSystem != ''}
                          id='id_f_Plate_idCoordinateSystem'
                          label={translate('label:PlateAddEditView.idCoordinateSystemNavName')}
                          value={store.idCoordinateSystem}
                          onChange={(event) => store.handleChange(event)}
                          data={store.CoordinateSystems}
                          name='idCoordinateSystem'>
                        </BaseLookup>
                      </Grid>

                      <Grid item md={12} xs={12}>
                        <ProtectedTextField
                          label={translate('label:ValuteAddEditView.description')}
                          name="description"
                          id="id_f_Valute_description"
                          onChange={(event) => store.handleChange(event)}
                          value={store.description}
                          helperText={store.errordescription}
                          error={store.errordescription != ''}
                        />
                      </Grid>
                      <Grid item md={12} xs={12}>
                        <ProtectedTextField
                          label={translate('label:ValuteAddEditView.code')}
                          name="code"
                          id="id_f_Valute_code"
                          onChange={(event) => store.handleChange(event)}
                          value={store.code}
                          helperText={store.errorcode}
                          error={store.errorcode != ''}
                        />
                      </Grid>
                      <Grid item md={12} xs={12}>
                        <ProtectedTextField
                          label={translate('label:ValuteAddEditView.queueNumber')}
                          name="queueNumber"
                          id="id_f_Valute_queueNumber"
                          onChange={(event) => store.handleChange(event)}
                          value={store.queueNumber}
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
