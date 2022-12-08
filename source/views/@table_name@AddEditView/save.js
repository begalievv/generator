import { userApiClient } from "src/components/ApiHelper";
import MainStore from "src/MainStore";
import i18n from 'i18next'
export function Save(store, props, handleErrorShow) {
  var data = {
    @|template_save_save|@
  };

  userApiClient('/@|table_name|@/AddOrUpdate', {
    method: "POST",
    body: data,
    headers: { "Content-type": "application/json; charset=UTF-8" }
  })
    .then(json => {
      if (store.id == 0) {
        MainStore.setSnackbar(i18n.t("message:snackbar.successSave"), 'success')
      } else {
        MainStore.setSnackbar(i18n.t("message:snackbar.successEdit"), 'success')
      }
      if (props.onBtnOkClick != null) {
        var id = json.id;
        props.onBtnOkClick(id, json);
      } else {
        props.navigate(process.env.REACT_APP_SUB_ROUTE + '/user/@|table_name|@', { replace: true })
      }
    })
    .catch(err => {
      if (store.id == 0) {
        MainStore.setSnackbar(i18n.t("message:snackbar.errorSave"), 'error')
      } else {
        MainStore.setSnackbar(i18n.t("message:snackbar.errorEdit"), 'error')
      }
      handleErrorShow(err.message)
    });
}
