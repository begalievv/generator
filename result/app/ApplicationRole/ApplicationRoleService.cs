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
    public partial class EmployeeService : BaseProtectedCrudService<EmployeeDto, int>, IEmployeeService
    {
        private readonly IEmployeeRepository _EmployeeRepository;
        private readonly IEmployeeRoleRepository _EmployeeRoleRepository;
        private readonly IApplicationRoleRepository _ApplicationRoleRepository;
        public EmployeeService(ISessionProvider sessionProvider,
            IAccessService accessService,
            IEmployeeRepository EmployeeRepository,
            IApplicationRoleRepository ApplicationRoleRepository,
            IEmployeeRoleRepository EmployeeRoleRepository) :
            base(EmployeeRepository,
                sessionProvider,
                accessService)
        {
            _EmployeeRepository = EmployeeRepository;
            _ApplicationRoleRepository = ApplicationRoleRepository;
            _EmployeeRoleRepository = EmployeeRoleRepository;
        }

        #region Access Keys
        protected override string AddMedtodKey => "Employee.Add";

        protected override string UpdateMedtodKey => "Employee.Update";

        protected override string RemoveMedtodKey => "Employee.Remove";

        protected override string ReadMedtodKey => "Employee.Read";
        #endregion

        protected override void ModelValidate(EmployeeDto dto, List<IExecutionError> errors)
        {
           
            base.ModelValidate(dto, errors);
        }

        protected override void DataValidate(EmployeeDto dto, List<IExecutionError> errors)
        {
            base.DataValidate(dto, errors);
        }

        #region Custom Add
        protected override int CustomAdd(EmployeeDto dto)
        {
          return base.CustomAdd(dto);
        }
        #endregion Custom Add

        #region Custom Update
        protected override int CustomUpdate(EmployeeDto updateDto)
        {
            return base.CustomUpdate(updateDto);
        }
        #endregion Custom Update

        public List<EmployeeDto> GetByidSex(int idSex)
        {
            _accessService.CheckAccess(_sessionProvider.UserId, _sessionProvider.UserName, ReadMedtodKey);
            return _EmployeeRepository.GetByidSex(idSex);
        }
    }
}