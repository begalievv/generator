import { userApiClient } from "src/components/ApiHelper";
import MainStore from "src/MainStore";
import i18n from 'i18next'
export function Save(store, props, handleErrorShow) {
  var data = {
		id: store.id - 0,
		name: store.name,
		description: store.description,
		code: store.code,
		queueNumber: store.queueNumber - 0
  };

userApiClient('/Valute/AddOrUpdate', {
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
        props.navigate(process.env.REACT_APP_SUB_ROUTE + '/user/Valute', { replace: true })
      }
    })
    .catch(err => {
      if(store.id == 0){
        MainStore.setSnackbar(i18n.t("message:snackbar.errorSave"), 'error')
      }else{
        MainStore.setSnackbar(i18n.t("message:snackbar.errorEdit"), 'error')
      }
      MainStore.setSnackbar(i18n.t("message:snackbar.errorSave"), 'error')
      handleErrorShow(err.message)
    });

}
