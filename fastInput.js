import React from 'react';
import { userRoleClient } from 'src/components/RoleHelper';
import { useNavigate } from 'react-router-dom';
import {
    Divider,
    Grid,
    Box,
    IconButton,
    Paper,
} from '@material-ui/core';

import BaseLookup from 'src/components/BaseLookup';
import ProtectedTextField from 'src/helpers/TextField.js';

import ProtectedCheckbox from 'src/helpers/Checkbox.js';
import ProtectedTimeField from 'src/helpers/TimeEdit.js';

import ProtectedButton from 'src/helpers/Button.js';
import { withTranslation } from 'react-i18next';
import CloseIcon from '@material-ui/icons/Close';
import DeleteIcon from '@material-ui/icons/Delete';
import CreateIcon from '@material-ui/icons/Create';
import InfoIcon from '@material-ui/icons/Info';
import i18n from 'i18next';

import CheckCircleOutlineOutlinedIcon from '@material-ui/icons/CheckCircleOutlineOutlined';
import CancelOutlinedIcon from '@material-ui/icons/CancelOutlined';

import SubtitlesOutlinedIcon from '@material-ui/icons/SubtitlesOutlined';
import DescriptionOutlinedIcon from '@material-ui/icons/DescriptionOutlined';
import CodeOutlinedIcon from '@material-ui/icons/CodeOutlined';
import DynamicFeedOutlinedIcon from '@material-ui/icons/DynamicFeedOutlined';

import MainStore from 'src/MainStore';
import store from "src/views/SpentMedicine/SpentMedicineListView/store"
import storeAddEdit from "src/views/SpentMedicine/SpentMedicineAddEditView/store"

import { observer } from "mobx-react"

const BaseView = observer(
    class BaseView extends React.Component {

        handleDialogClose = (yesNo) => {
            if (yesNo == true) {
                MainStore.onCloseConfirm()
                store.delete(store.currentId, (res) => {
                    store.loadSpentMedicinesCard(this.props.idMain)
                    store.loadMedicaments(this.props.idMain)
                    store.setCurrentId(0)
                })
            }
            else {
                store.setCurrentId(0)
                MainStore.onCloseConfirm()
            }
        }

        componentDidMount() {
            if (this.props.idMain == null) return;
            if (this.props.idMain == 0) return;

            storeAddEdit.idCard = this.props.idMain
            store.setFastInputIdMain(this.props.idMain);
            store.loadSpentMedicinesCard(this.props.idMain);
            store.loadMedicaments(this.props.idMain)
        }

        componentDidUpdate() {
            if (this.props.idMain == null) return;
            if (this.props.idMain == 0) return;
            if (this.props.idMain == store.fastInput.idMain) return;

            storeAddEdit.idCard = this.props.idMain
            store.setFastInputIdMain(this.props.idMain)
            store.loadSpentMedicinesCard(this.props.idMain);
            store.loadMedicaments(this.props.idMain)
        }


        render() {
            var roleName = 'SpentMedicine';
            var roles = userRoleClient();
            const { t } = this.props;
            const translate = t;


            const columns = [
                {
                    fieldName: 'idMedicamentNavName',
                    width: null //or number from 1 to 12
                },
                {
                    fieldName: 'amount',
                    width: null //or number from 1 to 12
                },

            ]

            return <Paper
                id="id_SpentMedicine"
                name='SpentMedicine'
                elevation={7} style={{
                    width: '100%',
                    padding: 25
                }}>
                <Box mb={3}>
                    <h2 name='SpentMedicineTitleName'>{translate("label:SpentMedicineListView.entityTitle")}</h2>
                </Box>
                <Grid
                    id="id_SpentMedicineTable"
                    name='SpentMedicineTable'
                    container
                    direction="column"
                >

                    <Grid
                        container
                        direction="row"
                        justifyContent="center"
                        alignItems="center"
                        spacing={1}
                        id="id_SpentMedicine_titleRow"
                        name='SpentMedicine_titleRow'
                    >

                        {columns.map(col => {
                            let id = "id_c_title_SpentMedicine_" + col.fieldName;
                            let name = col.fieldName;
                            let style = {
                                wordBreak: 'break-word',
                                whiteSpace: 'pre-wrap',
                            };
                            let label = translate('label:SpentMedicineAddEditView.' + col.fieldName)

                            if (col.width == null) {
                                return <Grid
                                    id={id}
                                    name={name}
                                    item xs
                                    style={style}
                                >
                                    <strong> {label}</strong>
                                </Grid>
                            }
                            else return <Grid
                                id={id}
                                name={name}
                                item xs={col.width}
                                style={style}
                            >
                                <strong> {label}</strong>
                            </Grid>

                        })}

                        <Grid item xs={1}></Grid>

                    </Grid>
                    <Divider />
                    {store.data.map(entity => {
                        var style = {};
                        if (entity.id === store.currentId) {
                            style = {
                                backgroundColor: '#F0F0F0',
                            };
                        }

                        return <>
                            <Grid
                                container
                                direction="row"
                                justifyContent="center"
                                alignItems="center"
                                style={style}
                                spacing={1}
                                id="id_SpentMedicine_row"
                                name='SpentMedicine_row'
                            >

                                {columns.map(col => {
                                    let id = "id_SpentMedicine_" + col.fieldName + "_value";
                                    let name = col.fieldName;
                                    let style = {
                                        wordBreak: 'break-word',
                                        whiteSpace: 'pre-wrap',
                                        marginTop: 5,
                                        marginBottom: 5
                                    };

                                    if (col.width == null) {
                                        return <Grid item xs
                                            style={style}
                                            name={name}
                                            id={id}
                                        >
                                            {entity[col.fieldName]}
                                        </Grid>
                                    }
                                    else return <Grid
                                        item
                                        xs={col.width}
                                        style={style}
                                        name={name}
                                        id={id}
                                    >
                                        {entity[col.fieldName]}
                                    </Grid>


                                })}

                                <Grid
                                    item
                                    xs={1}>
                                    {store.fastInput.isEdit === false && <>
                                        <IconButton
                                            id="id_SpentMedicineEditButton"
                                            name='edit_button'
                                            style={{ margin: 0, marginRight: 15, padding: 0 }}
                                            onClick={() => {
                                                store.setFastInputIsEdit(true)
                                                storeAddEdit.clearStore();
                                                storeAddEdit.setData(entity)
                                                // или storeAddEdit.doLoad(entity.id)
                                            }}>
                                            <CreateIcon />
                                        </IconButton>
                                        <IconButton
                                            id="id_SpentMedicineDeleteButton"
                                            name='delete_button'
                                            style={{ margin: 0, padding: 0 }}
                                            onClick={() => {

                                                store.setCurrentId(entity.id)
                                                MainStore.openErrorConfirm(
                                                    i18n.t('areYouSure'),
                                                    i18n.t('delete'),
                                                    i18n.t('cancel'),
                                                    () => { this.handleDialogClose(true) },
                                                    () => { this.handleDialogClose(false) })

                                            }}>
                                            <DeleteIcon />
                                        </IconButton>

                                    </>}
                                </Grid>
                            </Grid>
                            <Divider />
                        </>
                    })}


                    {store.fastInput.isEdit === true && <Paper
                        elevation={0}
                        style={{
                            backgroundColor: '#F0F0F0',
                            margin: 10,
                            padding: 10
                        }}>

                        <div>

                            <Grid
                                container
                                direction="row"
                                justifyContent="center"
                                alignItems="center"
                                spacing={1}
                            >
                                <Grid item md={4} xs={4}>
                                    <ProtectedTextField
                                        label={translate('label:SpentMedicineAddEditView.amountNavName')}
                                        name="amount"
                                        id="id_fi_SpentMedicine_amount"
                                        onChange={(event) => storeAddEdit.handleChange(event)}
                                        value={storeAddEdit.amount}
                                        type="number"
                                        helperText={storeAddEdit.erroramount}
                                        error={storeAddEdit.erroramount != ''}
                                        roleName={roleName + '.amount'}
                                    />
                                </Grid>
                                <Grid item md={8} xs={8}>
                                    <BaseLookup
                                        helperText={storeAddEdit.erroridMedicament}
                                        error={storeAddEdit.erroridMedicament != ''}
                                        roles={roles}
                                        required
                                        roleName={roleName + '.idMedicament'}
                                        id='id_fi_SpentMedicine_idMedicament'
                                        label={translate('label:SpentMedicineAddEditView.idMedicamentNavName')}
                                        value={storeAddEdit.idMedicament}
                                        onChange={(event) => storeAddEdit.handleChange(event)}
                                        data={store.dataMedicaments}
                                        name='idMedicament' variant='outlined'>
                                    </BaseLookup>
                                </Grid>
                            </Grid>
                            <Box ml={2}>
                                <IconButton
                                    style={{
                                        color: '#066a73',
                                    }}
                                    id="id_SpentMedicineSaveButton"
                                    name='SpentMedicineSaveButton'
                                    onClick={() => {
                                        storeAddEdit.idCard = this.props.idMain - 0
                                        storeAddEdit.onSaveClick({
                                            onBtnOkClick: () => {
                                                store.setFastInputIsEdit(false)
                                                store.setCurrentId(0)
                                                store.loadSpentMedicinesCard(this.props.idMain)
                                                store.loadMedicaments(this.props.idMain)
                                            }
                                        })
                                    }}
                                >
                                    <CheckCircleOutlineOutlinedIcon />
                                </IconButton>
                                <IconButton
                                    id="id_SpentMedicineCancelButton"
                                    name='SpentMedicineCancelButton'
                                    style={{
                                        color: "#000000",
                                    }}
                                    onClick={() => {
                                        store.setFastInputIsEdit(false)
                                        store.setCurrentId(0)
                                        storeAddEdit.clearStore()
                                    }}
                                >
                                    <CancelOutlinedIcon />
                                </IconButton>
                            </Box>


                        </div>
                    </Paper>
                    }

                    {store.fastInput.isEdit === false && <Grid item xs={3}>
                        <ProtectedButton
                            size="small"
                            color="add"
                            variant="contained"
                            style={{ marginTop: 20 }}
                            id="id_SpentMedicineAddButton"
                            name='SpentMedicineAddButton'
                            onClick={() => {
                                store.setFastInputIsEdit(true)
                                store.setCurrentId(0)
                                storeAddEdit.clearStore();
                            }}
                        >
                            {translate("common:add")}
                        </ProtectedButton>
                    </Grid>
                    }
                </Grid>
            </Paper>

        }

    }
)
function MtmView(props) {
    let navigate = useNavigate();
    return <BaseView {...props} navigate={navigate} />;
}

export default withTranslation()(MtmView);
