# Larder and Meals Implementation Plan

## Current State Analysis

### Shopping Implementation (Reference)

- **Backend**: Complete API with GET, POST, PUT, DELETE endpoints
- **Data Layer**: Both `DataLayer` and `CosmosDataLayer` implementations
- **Frontend**: Full CRUD functionality with real-time updates
- **Database**: Cosmos DB containers with proper schema
- **Features**: Add items, edit names, toggle checkboxes, clear completed items

### Current Larder State

- **Backend**: API endpoints exist but incomplete (missing PUT/DELETE)
- **Data Layer**: Methods exist but inconsistent with shopping implementation
- **Frontend**: HTML structure exists, no JavaScript functionality
- **Database**: Cosmos container exists with schema

### Current Meals State

- **Backend**: API endpoints exist but incomplete (missing PUT/DELETE)
- **Data Layer**: Methods exist but inconsistent with shopping implementation
- **Frontend**: HTML structure exists, no JavaScript functionality
- **Database**: Cosmos container exists with schema

## Implementation Plan

### Phase 1: Backend Consistency (High Priority)

1. **Fix Data Layer Inconsistencies**

   - Update `DataLayer` to match shopping implementation pattern
   - Ensure consistent response formats across all item types
   - Fix method signatures to match shopping pattern

2. **Complete API Endpoints**

   - Add missing PUT endpoints for larder and meals
   - Add missing DELETE endpoints for larder and meals
   - Ensure consistent error handling and validation

3. **Database Schema Alignment**

   - Verify Cosmos containers match documented schema
   - Ensure consistent field naming (e.g., `inCart` vs `reorder`)

### Phase 2: Frontend Larder Implementation (High Priority)

1. **JavaScript Functions**

   - `loadLarderItems()` - Load items from API
   - `saveLarderItem()` - Save individual item
   - `addLarderItem()` - Add new item
   - `renderLarderTable()` - Render table with items
   - `clearReorderItems()` - Clear items marked for reorder

2. **Event Listeners**

   - Add item button functionality
   - Input field editing (blur/enter)
   - Checkbox toggle for reorder status
   - Clear reorder button functionality

3. **UI Integration**

   - Connect HTML buttons to JavaScript functions
   - Implement real-time updates
   - Add proper error handling and status messages

### Phase 3: Frontend Meals Implementation (Medium Priority)

1. **JavaScript Functions**

   - `loadMealItems()` - Load meals from API
   - `saveMealItem()` - Save individual meal
   - `addMealItem()` - Add new meal
   - `renderMealTable()` - Render table with meals
   - `deleteMealItem()` - Delete meal functionality

2. **Event Listeners**

   - Add meal button functionality
   - Meal name and ingredients editing
   - Delete meal functionality

3. **UI Integration**

   - Connect HTML elements to JavaScript functions
   - Implement meal editing capabilities
   - Add proper validation

### Phase 4: Testing and Refinement (Low Priority)

1. **Cross-browser Testing**
2. **Error Handling Validation**
3. **Performance Optimization**
4. **Code Cleanup**

## Technical Details

### Data Structure Consistency

- **Larder Items**: `{id, name, reorder, createdAt, modifiedAt}`
- **Meal Items**: `{id, name, ingredients, createdAt, modifiedAt}`
- **Shopping Items**: `{id, name, inCart, createdAt, modifiedAt}`

### API Response Format

```json
{
  "success": true,
  "message": "Item added successfully",
  "item": { /* item data */ }
}
```

### Frontend State Management

- Global arrays: `larderItems[]`, `mealItems[]`
- Consistent sorting: unchecked/false items first
- Real-time updates on changes

## Potential Issues to Address

1. **Data Layer Architecture Conflict**

   - Current implementation has two data layers (`DataLayer` and `CosmosDataLayer`)
   - Need to determine which one to use consistently
   - Shopping uses `CosmosDataLayer` pattern

2. **API Response Inconsistency**

   - Shopping API returns items directly in array format
   - Larder/Meals API returns wrapped response format
   - Need to standardize response formats

3. **Frontend State Management**

   - Shopping uses client-side state management
   - Need to implement similar pattern for larder and meals
   - Consider optimistic updates vs server-side validation

## General Improvements (Post-Implementation)

1. **Code Organization**

   - Extract common functionality into shared modules
   - Implement consistent error handling patterns
   - Add input validation and sanitization

2. **User Experience**

   - Add loading states during API calls
   - Implement keyboard shortcuts
   - Add confirmation dialogs for destructive actions

3. **Performance**

   - Implement debounced saving for text inputs
   - Add caching for frequently accessed data
   - Optimize database queries

4. **Maintainability**

   - Add comprehensive error logging
   - Implement unit tests for critical functions
   - Add API documentation

5. **Feature Enhancements**

   - Add bulk operations (select multiple items)
   - Implement search/filter functionality
   - Add drag-and-drop reordering
   - Implement data export/import

## Implementation Order

1. Fix backend data layer inconsistencies
2. Complete missing API endpoints
3. Implement larder frontend functionality
4. Implement meals frontend functionality
5. Add testing and refinement
6. Apply general improvements

This plan ensures that larder and meals functionality matches the shopping implementation while maintaining code consistency and user experience.