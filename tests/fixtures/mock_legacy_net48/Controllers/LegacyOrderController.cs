using System.Web.Mvc;
using System.Threading.Tasks;

namespace LegacyEnterpriseApp.Controllers
{
    [Route("legacy/orders")]
    public class LegacyOrderController : Controller
    {
        [HttpGet]
        public ActionResult Index()
        {
            return View();
        }

        [HttpPost]
        [Route("process")]
        public async Task<ActionResult> ProcessLegacyOrder(int orderId, decimal amount)
        {
            if (orderId <= 0)
                return BadRequest("Invalid order id");
            if (amount <= 0)
                return BadRequest("Amount must be greater than zero");
            return Json(new { success = true });
        }
    }
}
