import { FC, useEffect } from 'react';
import @|table_name_pascal|@AddEditBaseView from './base';
import store from "./store"
import { observer } from "mobx-react"
import { Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';
import { useTranslation } from 'react-i18next';
import CustomButton from 'components/Button';

type PopupFormProps = {
  openPanel: boolean;
  id: number;
  onBtnCancelClick: () => void;
  onSaveClick: (id: number) => void;
}

const @|table_name_pascal|@PopupForm: FC<PopupFormProps> = observer((props) => {
  const { t } = useTranslation();
  const translate = t;

  useEffect(() => {
    if (props.openPanel) {
      store.doLoad(props.id)
    } else {
      store.clearStore()
    }
  }, [props.openPanel])

  return (
    <Dialog open={props.openPanel} onClose={props.onBtnCancelClick} maxWidth="sm" fullWidth>
      <DialogTitle>{translate('label:@|table_name_pascal|@AddEditView.entityTitle')}</DialogTitle>
      <DialogContent>
        <@|table_name_pascal|@AddEditBaseView
          isPopup={true}
        >
        </@|table_name_pascal|@AddEditBaseView>
      </DialogContent>
      <DialogActions>
        <DialogActions>
          <CustomButton
            variant="contained"
            id="id_@|table_name_pascal|@SaveButton"
            name={'@|table_name_pascal|@AddEditView.save'}
            onClick={() => {
              store.onSaveClick((id: number) => props.onSaveClick(id))
            }}
          >
            {translate("common:save")}
          </CustomButton>
          <CustomButton
            variant="contained"
            id="id_@|table_name_pascal|@CancelButton"
            name={'@|table_name_pascal|@AddEditView.cancel'}
            onClick={() => props.onBtnCancelClick()}
          >
            {translate("common:cancel")}
          </CustomButton>
        </DialogActions>
      </DialogActions >
    </Dialog >
  );
})

export default @|table_name_pascal|@PopupForm
