import React, { FC } from "react";
import { Grid } from "@mui/material";
import { useTranslation } from "react-i18next";
import { observer } from "mobx-react";
import { withForm } from "components/hoc/withForm";
import @|table_name_pascal|@AddEditBaseView from "./base";
import store from "./store";
import MtmTabs from "./mtmTabs";

interface @|table_name_pascal|@Props {
  id: string | null;
}

const @|table_name_pascal|@AddEditView: FC<@|table_name_pascal|@Props> = observer((props) => {
  const { t } = useTranslation();
  const { id } = props;

  return (
    <@|table_name_pascal|@AddEditBaseView>
      {/* Show many-to-many relationship tabs only when editing existing @|table_name_pascal|@ */}
      {Number(id) > 0 && (
        <Grid item xs={12} spacing={0}>
          <MtmTabs />
        </Grid>
      )}
    </@|table_name_pascal|@AddEditBaseView>
  );
})

export default withForm(@|table_name_pascal|@AddEditView, store, "/user/@|table_name_pascal|@");