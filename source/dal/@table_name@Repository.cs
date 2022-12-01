using App.General;
using DAL.EF.Context;
using DAL.Base;
using Core.Abstraction;
using App;
using DAL.EF.Entities;
using LayerTransmitter.Wrapper;
using System.Collections.Generic;
using System.Linq.Expressions;
using System;
using System.Security.Cryptography.X509Certificates;
using System.Linq;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;
using ErrorIdentity;
using Flurl;
using Flurl.Http;
using DAL.Access;
using App.Access;

namespace DAL.General
{
    public class EmployeeRepository : BaseEfCrudRepository<EmployeeDto, int, Employee>, IEmployeeRepository
    {
        public ISystemSettingProvider SystemSettingProvider { get; }

        public EmployeeRepository(ApplicationContext context, ISystemSettingProvider systemSettingProvider)
            : base(context)
        {
            SystemSettingProvider = systemSettingProvider;
        }

        protected override Func<EmployeeDto, Employee> entitySelector => (EmployeeDto x) => x.ToEmployee();

        protected override Expression<Func<EmployeeDto, Employee>> entitySelectorExpr => (EmployeeDto x) => x.ToEmployee();

        protected override Func<Employee, EmployeeDto> dtoSelector => (Employee x) => x.ToEmployeeDto();

        protected override Expression<Func<Employee, EmployeeDto>> dtoSelectorExpr => (Employee x) => x.ToEmployeeDto();

        protected override Expression<Func<Employee, bool>> filterSameItemsExpr(EmployeeDto dto)
        {
            return x => false;
            // Уточнить у аналитика , по каким параметрам проверяется наличие дублиатат записи в БД и реализовать 
            // sample return x => false;  если нет проверки на дублирование 
            // Или
            // sample return x => (x.code != null && x.code == dto.Code) || x.name == dto.Name;
        }

        protected override IQueryable<Employee> TheWholeEntities => context.Employees
            .AsNoTracking()
        ;

        public List<EmployeeDto> GetByidSex(int idSex)
        {
            return GetByFilter(x => x.idSex == idSex);
        }
    }
}
