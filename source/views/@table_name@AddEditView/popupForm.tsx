import { FC, useEffect } from 'react';
import @|table_name|@AddEditBaseView from './base';
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

const @|table_name|@PopupForm: FC<PopupFormProps> = observer((props) => {
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
      <DialogTitle>{translate('label:@|table_name|@AddEditView.entityTitle')}</DialogTitle>
      <DialogContent>
        <@|table_name|@AddEditBaseView
          isPopup={true}
        >
        </@|table_name|@AddEditBaseView>
      </DialogContent>
      <DialogActions>
        <DialogActions>
          <CustomButton
            variant="contained"
            id="id_@|table_name|@SaveButton"
            name={'@|table_name|@AddEditView.save'}
            onClick={() => {
              store.onSaveClick((id: number) => props.onSaveClick(id))
            }}
          >
            {translate("common:save")}
          </CustomButton>
          <CustomButton
            variant="contained"
            id="id_@|table_name|@CancelButton"
            name={'@|table_name|@AddEditView.cancel'}
            onClick={() => props.onBtnCancelClick()}
          >
            {translate("common:cancel")}
          </CustomButton>
        </DialogActions>
      </DialogActions >
    </Dialog >
  );
})

export default @|table_name|@PopupForm
