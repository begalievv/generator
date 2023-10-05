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
import store from "src/views/@|table_name|@/@|table_name|@ListView/store"
import storeAddEdit from "src/views/@|table_name|@/@|table_name|@AddEditView/store"

import { observer } from "mobx-react"

const BaseView = observer(
    class BaseView extends React.Component {

        handleDialogClose = (yesNo) => {
            if (yesNo == true) {
                MainStore.onCloseConfirm()
                store.delete(store.currentId, (res) => {
                    @|template_store_load_function|@
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

            @|template_fast_input_change_main_id|@
            store.setFastInputIdMain(this.props.idMain);
            @|template_store_load_function|@
            @|template_fast_input_load_dicts|@
        }

        componentDidUpdate() {
            if (this.props.idMain == null) return;
            if (this.props.idMain == 0) return;
            if (this.props.idMain == store.fastInput.idMain) return;

            @|template_fast_input_change_main_id|@
            store.setFastInputIdMain(this.props.idMain)
            @|template_store_load_function|@
        }


        render() {
            var roleName = '@|table_name|@';
            var roles = userRoleClient();
            const { t } = this.props;
            const translate = t;


            const columns = [
                @|template_fast_input_columns|@
            ]

            return <Paper
                id="id_@|table_name|@"
                name='@|table_name|@'
                elevation={7} style={{
                    width: '100%',
                    padding: 25
                }}>
                <Box mb={3}>
                    <h2 name='@|table_name|@TitleName'>{translate("label:@|table_name|@ListView.entityTitle")}</h2>
                </Box>
                <Grid
                    id="id_@|table_name|@Table"
                    name='@|table_name|@Table'
                    container
                    direction="column"
                >

                    <Grid
                        container
                        direction="row"
                        justifyContent="center"
                        alignItems="center"
                        spacing={1}
                        id="id_@|table_name|@_titleRow"
                        name='@|table_name|@_titleRow'
                    >

                        {columns.map(col => {
                            let id = "id_c_title_@|table_name|@_" + col.fieldName;
                            let name = col.fieldName;
                            let style = {
                                wordBreak: 'break-word',
                                whiteSpace: 'pre-wrap',
                            };
                            let label = translate('label:@|table_name|@AddEditView.' + col.fieldName)

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
                                id="id_@|table_name|@_row"
                                name='@|table_name|@_row'
                            >

                                {columns.map(col => {
                                    let id = "id_@|table_name|@_" + col.fieldName + "_value";
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
                                            id="id_@|table_name|@EditButton"
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
                                            id="id_@|table_name|@DeleteButton"
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
                                @|template_fastinput_fields|@
                            </Grid>
                            <Box ml={2}>
                                <IconButton
                                    style={{
                                        color: '#066a73',
                                    }}
                                    id="id_@|table_name|@SaveButton"
                                    name='@|table_name|@SaveButton'
                                    onClick={() => {
                                        @|template_fast_input_change_main_id|@
                                        storeAddEdit.onSaveClick({
                                            onBtnOkClick: () => {
                                                store.setFastInputIsEdit(false)
                                                store.setCurrentId(0)
                                                @|template_store_load_function|@
                                            }
                                        })
                                    }}
                                >
                                    <CheckCircleOutlineOutlinedIcon />
                                </IconButton>
                                <IconButton
                                    id="id_@|table_name|@CancelButton"
                                    name='@|table_name|@CancelButton'
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
                            id="id_@|table_name|@AddButton"
                            name='@|table_name|@AddButton'
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
