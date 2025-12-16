/**
 * Icon System Usage Examples
 * 
 * Demonstrates how to use embedded icons in your Arduino sketches
 */

#include "system_utils.h"
#include <Adafruit_SSD1306.h>

// OLED display instance
Adafruit_SSD1306 display(128, 64, &Wire, -1);

void setup() {
    Serial.begin(115200);
    
    // Initialize OLED
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println("OLED init failed");
        while(1);
    }
    
    // Icon system works immediately - no initialization needed
    // (initIconSystem() only needed for LittleFS fallback)
    
    display.clearDisplay();
    
    // Example 1: Simple icon drawing
    example_basic_icons();
    
    // Example 2: Icon grid
    example_icon_grid();
    
    // Example 3: Icon with text
    example_icon_with_text();
    
    // Example 4: Conditional icon display
    example_conditional_icons();
    
    // Example 5: Custom rendering
    example_custom_rendering();
}

void loop() {
    // Icons can be used in loop as well
    display.clearDisplay();
    
    // Animated icon example
    static int x = 0;
    drawIcon(&display, "folder", x, 28, WHITE);
    x = (x + 2) % 112;  // 128 - 16
    
    display.display();
    delay(50);
}

// Example 1: Basic icon drawing
void example_basic_icons() {
    display.clearDisplay();
    
    // Draw icons at different positions
    drawIcon(&display, "folder", 0, 0, WHITE);
    drawIcon(&display, "file", 20, 0, WHITE);
    drawIcon(&display, "wifi", 40, 0, WHITE);
    drawIcon(&display, "settings", 60, 0, WHITE);
    
    display.display();
    delay(2000);
}

// Example 2: Icon grid layout
void example_icon_grid() {
    display.clearDisplay();
    
    const char* icons[] = {"folder", "file", "wifi", "settings"};
    int iconCount = 4;
    int cols = 4;
    int spacing = 24;
    
    for (int i = 0; i < iconCount; i++) {
        int x = (i % cols) * spacing + 8;
        int y = (i / cols) * spacing + 8;
        drawIcon(&display, icons[i], x, y, WHITE);
    }
    
    display.display();
    delay(2000);
}

// Example 3: Icon with text label
void example_icon_with_text() {
    display.clearDisplay();
    
    // Icon + label pattern
    drawIcon(&display, "folder", 10, 10, WHITE);
    display.setCursor(30, 14);
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.print("Documents");
    
    drawIcon(&display, "file", 10, 30, WHITE);
    display.setCursor(30, 34);
    display.print("readme.txt");
    
    display.display();
    delay(2000);
}

// Example 4: Conditional icon display with fallback
void example_conditional_icons() {
    display.clearDisplay();
    
    // Check if icon exists before drawing
    if (iconExists("wifi")) {
        drawIcon(&display, "wifi", 10, 10, WHITE);
    } else {
        // Fallback to text
        display.setCursor(10, 10);
        display.print("[WIFI]");
    }
    
    // Try to draw icon, fallback on failure
    if (!drawIcon(&display, "unknown_icon", 10, 30, WHITE)) {
        display.setCursor(10, 30);
        display.print("[???]");
    }
    
    display.display();
    delay(2000);
}

// Example 5: Custom rendering with raw bitmap data
void example_custom_rendering() {
    display.clearDisplay();
    
    uint8_t buffer[32];
    uint8_t width, height;
    
    if (loadIconData("folder", buffer, sizeof(buffer), width, height)) {
        // Custom rendering - invert colors
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int byteIndex = (y * width + x) / 8;
                int bitIndex = (y * width + x) % 8;
                bool pixel = buffer[byteIndex] & (1 << bitIndex);
                
                // Draw inverted
                display.drawPixel(x + 10, y + 10, pixel ? BLACK : WHITE);
            }
        }
        
        display.setCursor(30, 14);
        display.print("Inverted");
    }
    
    display.display();
    delay(2000);
}

// Bonus: Status bar with icons
void drawStatusBar() {
    // WiFi status
    if (WiFi.status() == WL_CONNECTED) {
        drawIcon(&display, "wifi", 0, 0, WHITE);
    }
    
    // Battery/power icon
    drawIcon(&display, "battery", 112, 0, WHITE);
    
    // Time in center
    display.setCursor(40, 2);
    display.setTextSize(1);
    display.print("12:34");
}

// Bonus: File browser UI
void drawFileBrowser() {
    display.clearDisplay();
    
    // Title
    display.setCursor(0, 0);
    display.setTextSize(1);
    display.print("Files");
    
    // File list with icons
    const char* files[] = {"Documents", "Photos", "readme.txt"};
    const char* icons[] = {"folder", "folder", "file"};
    
    for (int i = 0; i < 3; i++) {
        int y = 16 + i * 16;
        drawIcon(&display, icons[i], 4, y, WHITE);
        display.setCursor(24, y + 4);
        display.print(files[i]);
    }
    
    display.display();
}

// Bonus: Menu system with icons
void drawMenu() {
    display.clearDisplay();
    
    struct MenuItem {
        const char* icon;
        const char* label;
    };
    
    MenuItem menu[] = {
        {"settings", "Settings"},
        {"wifi", "Network"},
        {"sensor", "Sensors"},
        {"info", "About"}
    };
    
    int selected = 0;  // Currently selected item
    
    for (int i = 0; i < 4; i++) {
        int y = i * 16;
        
        // Highlight selected item
        if (i == selected) {
            display.fillRect(0, y, 128, 16, WHITE);
            drawIcon(&display, menu[i].icon, 4, y + 2, BLACK);
            display.setTextColor(BLACK);
        } else {
            drawIcon(&display, menu[i].icon, 4, y + 2, WHITE);
            display.setTextColor(WHITE);
        }
        
        display.setCursor(24, y + 4);
        display.print(menu[i].label);
    }
    
    display.display();
}
