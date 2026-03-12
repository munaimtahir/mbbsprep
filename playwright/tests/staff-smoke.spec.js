const { test, expect } = require('@playwright/test');

const staffCredentials = {
  username: process.env.PLAYWRIGHT_STAFF_USERNAME || 'playwright_staff',
  password: process.env.PLAYWRIGHT_STAFF_PASSWORD || 'PlaywrightStaff123!',
};

test('staff user can sign in to the backoffice', async ({ page }) => {
  await page.goto('/staff/login/');
  await page.locator('#id_username').fill(staffCredentials.username);
  await page.locator('#id_password').fill(staffCredentials.password);
  await page.getByRole('button', { name: 'Login' }).click();

  await expect(page).toHaveURL(/\/staff\/$/);
  await expect(page.locator('body')).toContainText('Dashboard');
});
