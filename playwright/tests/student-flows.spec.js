const { test, expect } = require('@playwright/test');

const studentCredentials = {
  username: process.env.PLAYWRIGHT_STUDENT_USERNAME || 'playwright_student',
  password: process.env.PLAYWRIGHT_STUDENT_PASSWORD || 'PlaywrightPass123!',
};

async function login(page) {
  await page.goto('/login/');
  await page.getByLabel('Email or Username').fill(studentCredentials.username);
  await page.getByLabel('Password').fill(studentCredentials.password);
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page).toHaveURL(/\/dashboard\/$/);
}

test('student can sign in and view dashboard resources', async ({ page }) => {
  await login(page);
  await expect(page.locator('body')).toContainText('Dashboard');

  await page.goto('/resources/');
  await expect(page.locator('body')).toContainText('Study Resources');

  await page.goto('/subscription/payment/status/');
  await expect(page.locator('body')).toContainText('Payment Status');
});

test('student can open quiz start flow', async ({ page }) => {
  await login(page);
  await page.goto('/quiz/');
  await expect(page.locator('body')).toContainText('Quiz');

  await page.getByRole('link', { name: 'Start Quiz' }).first().click();
  await expect(page.locator('body')).toContainText('Start Quiz');
});
