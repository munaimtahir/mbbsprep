const { test, expect } = require('@playwright/test');

test.describe('public smoke', () => {
  const publicPages = [
    ['/', 'MedPrep'],
    ['/login/', 'Login to MedPrep'],
    ['/signup/', 'Sign Up for MedPrep'],
    ['/about/', 'About'],
    ['/contact/', 'Contact'],
    ['/faq/', 'FAQ'],
    ['/subscribe/', 'Subscription'],
    ['/resources/', 'Study Resources'],
    ['/staff/login/', 'Admin'],
  ];

  for (const [path, text] of publicPages) {
    test(`renders ${path}`, async ({ page }) => {
      await page.goto(path);
      await expect(page.locator('body')).toContainText(text);
    });
  }
});
