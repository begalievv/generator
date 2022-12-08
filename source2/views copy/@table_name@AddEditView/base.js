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
import ProtectedDateTimeField from 'src/helpers/DateTimeEdit';
import ProtectedCheckbox from 'src/helpers/Checkbox.js';
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

            <form id="id_@|table_name|@Form" name="name_@|table_name|@Form" autoComplete='off' noValidate>
              <Paper elevation={7} style={{ width: '100%' }}>
                <Card>
                  <CardHeader className={this.props.classes.header} title={<span id="id_f_@|table_name|@_title_name">{translate('label:@|table_name|@AddEditView.entityTitle')}</span>} />
                  <Divider />
                  <CardContent>
                    <Grid container xs={12} spacing={3} style={{ margin: 0 }}>
                      @|template_base_fields|@
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

function @|table_name|@AddEditBaseView(props) {
  let navigate = useNavigate();
  let query = useQuery();
  let classes = useStyles();
  return <BaseView {...props} navigate={navigate} classes={classes} />;
}

export default withTranslation()(@|table_name|@AddEditBaseView);
