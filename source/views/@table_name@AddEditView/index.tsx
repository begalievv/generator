import { FC, useEffect } from "react";
import { default as @|table_name|@AddEditBaseView } from './base'
import { useNavigate } from 'react-router-dom';
import { useLocation } from "react-router";
import { Box, Grid } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { observer } from "mobx-react"
import store from "./store"
import CustomButton from 'components/Button';
import MtmTabs from "./mtmTabs";

type @|table_name|@Props = {};

const @|table_name|@AddEditView: FC<@|table_name|@Props> = observer((props) => {
  const { t } = useTranslation();
  const translate = t;
  const navigate = useNavigate();
  const query = useQuery();
  const id = query.get("id")

  useEffect(() => {
    if ((id != null) &&
      (id !== '') &&
      !isNaN(Number(id.toString()))) {
      store.doLoad(Number(id))
    } else {
      navigate('/error-404')
    }
    return () => {
      store.clearStore()
    }
  }, [])

  return (
    <@|table_name|@AddEditBaseView {...props}>

      @|template_mtm_has_mtm|@
    
      <Grid item xs={12} spacing={0}>
        <Box display="flex" p={2}>
          <Box m={2}>
            <CustomButton
              variant="contained"
              id="id_@|table_name|@SaveButton"
              name={'@|table_name|@AddEditView.save'}
              onClick={() => {
                store.onSaveClick((id: number) => {
                  navigate('/user/@|table_name|@')
                })
              }}
            >
              {translate("common:save")}
            </CustomButton>
          </Box>
          <Box m={2}>
            <CustomButton
              variant="contained"
              id="id_@|table_name|@CancelButton"
              name={'@|table_name|@AddEditView.cancel'}
              onClick={() => navigate('/user/@|table_name|@')}
            >
              {translate("common:cancel")}
            </CustomButton>
          </Box>
        </Box>
      </Grid>
    </@|table_name|@AddEditBaseView>
  );
})

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

export default @|table_name|@AddEditView