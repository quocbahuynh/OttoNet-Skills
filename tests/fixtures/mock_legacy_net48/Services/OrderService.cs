using System.Data;
using System.Threading.Tasks;
using Dapper;

namespace LegacyEnterpriseApp.Services
{
    public class OrderService
    {
        private readonly IDbConnection _db;

        public OrderService(IDbConnection db)
        {
            _db = db;
        }

        public async Task<decimal> CalculateOrderTotal(int orderId)
        {
            // Direct Stored Procedure execution
            var taxRate = await _db.ExecuteScalarAsync<decimal>("sp_CalculateLegacyTax", new { OrderId = orderId }, commandType: CommandType.StoredProcedure);
            decimal subtotal = 1000m;
            decimal total = subtotal * (1 + taxRate);
            return total;
        }

        public async Task<object> GetOrderWithCustomer(int orderId)
        {
            const string sql = @"
                SELECT o.Id, o.Total, c.CompanyName 
                FROM [dbo].[Orders] o 
                INNER JOIN Customers c ON o.CustomerId = c.Id 
                WHERE o.Id = @OrderId AND o.Status = @Status";
            return await _db.QueryFirstOrDefaultAsync(sql, new { OrderId = orderId, Status = 1 });
        }

        public async Task CreateInvoice(int orderId, decimal amount)
        {
            const string insertSql = "INSERT INTO [Invoices] (OrderId, Amount) VALUES (@OrderId, @Amount)";
            await _db.ExecuteAsync(insertSql, new { OrderId = orderId, Amount = amount });
        }
    }
}
