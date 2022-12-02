using Core.Abstraction;
using Core.Services.BaseCrudService;
using App.Base;
using LayerTransmitter.Wrapper;
using System.Collections.Generic;
using Core.Validation;
using System;
using App.Access;

namespace App.General
{
    public partial class @|table_name|@Service : BaseProtectedCrudService<@|table_name|@Dto, int>, I@|table_name|@Service
    {
        private readonly I@|table_name|@Repository _@|table_name|@Repository;
        public @|table_name|@Service(ISessionProvider sessionProvider,
            IAccessService accessService,
            I@|table_name|@Repository @|table_name|@Repository):
            base(@|table_name|@Repository,
                sessionProvider,
                accessService)
        {
            _@|table_name|@Repository = @|table_name|@Repository;
        }

        #region Access Keys
        protected override string AddMedtodKey => "@|table_name|@.Add";
        protected override string UpdateMedtodKey => "@|table_name|@.Update";
        protected override string RemoveMedtodKey => "@|table_name|@.Remove";
        protected override string ReadMedtodKey => "@|table_name|@.Read";
        #endregion Access Keys

        #region Validation
        protected override void ModelValidate(@|table_name|@Dto dto, List<IExecutionError> errors)
        {
            base.ModelValidate(dto, errors);
        }
        protected override void DataValidate(@|table_name|@Dto dto, List<IExecutionError> errors)
        {
            base.DataValidate(dto, errors);
        }
        #endregion Validation

        #region Custom Add
        protected override int CustomAdd(@|table_name|@Dto dto)
        {
          return base.CustomAdd(dto);
        }
        #endregion Custom Add

        #region Custom Update
        protected override int CustomUpdate(@|table_name|@Dto updateDto)
        {
            return base.CustomUpdate(updateDto);
        }
        #endregion Custom Update

        #region Constraints
        @|template_service|@
        #endregion Constraints
    }
}