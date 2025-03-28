import React, { FC } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  Divider,
  Paper,
  Grid,
  Container,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import store from "./store"
import { observer } from "mobx-react"
import LookUp from 'components/LookUp';
import CustomTextField from "components/TextField";
import CustomCheckbox from "components/Checkbox";
import DateTimeField from "components/DateTimeField";

type @|table_name_pascal|@TableProps = {
  children ?: React.ReactNode;
  isPopup ?: boolean;
};

const Base@|table_name_pascal|@View: FC<@|table_name_pascal|@TableProps> = observer((props) => {
  const { t } = useTranslation();
  const translate = t;
  return (
    <Container maxWidth='xl' sx={{ mt: 3 }}>
      <Grid container spacing={3}>
        <Grid item md={props.isPopup ? 12 : 6}>
          <form data-testid="@|table_name_pascal|@Form" id="@|table_name_pascal|@Form" autoComplete='off'>
            <Card component={Paper} elevation={5}>
              <CardHeader title={
                <span id="@|table_name_pascal|@_TitleName">
                  {translate('label:@|table_name_pascal|@AddEditView.entityTitle')}
                </span>
              } />
              <Divider />
              <CardContent>
                <Grid container spacing={3}>
                  @|template_base_fields|@
                </Grid>
              </CardContent>
            </Card>
          </form>
        </Grid>
        {props.children}
      </Grid>
    </Container>
  );
})

export default Base@|table_name_pascal|@View;
